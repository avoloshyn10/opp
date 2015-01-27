#!/usr/bin/python

import openpanzer as op
from oppSql import *
from oppRdf import *
import util
from dbpedia import DbpediaQuery
from websearch import GoogleQuery, BingQuery
from urllib import quote, unquote
from pprint import pprint
import time,os, sys, errno

reload(sys)
sys.setdefaultencoding("utf-8")

OFFLINE_JSON_DIR = "../oppedia-offline"

eq = op.Equipment()
#eq.loadAllCountries()
eq.loadCountry(8) # Germany

print "Loaded %d units" % len(eq.eq)

# Finds a RDF resource URL based on a search string and a search provider
def searchRdfResource(searchString, provider=PROVIDER_DBPEDIA):

    qdbpedia = DbpediaQuery()
    qsearch = qdbpedia

    if provider == PROVIDER_GOOGLE or provider == PROVIDER_GOOGLE_SPECIFIC:
        qsearch = GoogleQuery()

    if provider == PROVIDER_BING:
        qsearch = BingQuery()

    r = qsearch.queryText(searchString)

    if len(r) == 0:
        print "Query %s with provider %s returned no results" % (searchString, provider)
        return None

    if provider == PROVIDER_DBPEDIA:
        rdfResource = unquote(r[0])
    else:
        rdfResource = util.wikiToDBpedia(r[0])

    # Web search returned resource might be a DBpedia redirect
    if provider != PROVIDER_DBPEDIA:
        tmp = qdbpedia.getRealUri(rdfResource) # resolve dbpedia redirect
        if tmp is not None:
            rdfResource = tmp
            print "Resolved resource redirect to %s" % rdfResource

    if rdfResource == "":
        print "Empty resource returned"
        return None

    rdfData = qdbpedia.getFromResource(rdfResource)

    if len(rdfData) == 0:
        print "No DBpedia data for %s resource" % rdfResource
        return None

    label = rdfData[0]["label"]["value"]
    print "Provider %s found label %s for resource %s" % (provider, label, rdfResource)

    return { "label": label, "resource": rdfResource }

@db_session
def createSqlResourceSearch(unitId, searchString, rdfdb, provider=PROVIDER_DBPEDIA):

    s = None

    result = searchRdfResource(searchString, provider)
    if result is not None:
        url = result["resource"]
        if rdfdb.load(url):
            s = ResourceSearch(unitId = unitId, provider = provider, searchString = searchString, foundResource = url)
            commit()
            if s is None:
                return None
        else:
            print "Cannot save RDF resource %s to DB" % url
            return None

        return { "sqlResource": s, "searchResult": result }

    return None


@db_session
def createSqlUnit(unit, rdfdb):

    print "Creating Unit %s (%d)" % (unit.getFullName(), unit.id)

    dbpediaSearch = util.unitNameToRegex(unit.getNicerName())
    webSearch = unit.getNicerName() + " " + unit.getClassName()

    dbpediaResult = createSqlResourceSearch(unit.id, dbpediaSearch, rdfdb, provider=PROVIDER_DBPEDIA)

    try:
        webResult = createSqlResourceSearch(unit.id, webSearch, rdfdb, provider=PROVIDER_GOOGLE)
    except:
        print "No Google results, trying Bing"
        try:
            webResult = createSqlResourceSearch(unit.id, webSearch, rdfdb, provider=PROVIDER_BING)
        except:
            print "No Web search results. Aborting unit creation"
            return True

    chosenResource = None
    chosenResult = None

    if dbpediaResult is not None:
        chosenResult = dbpediaResult["searchResult"]
        chosenResource = dbpediaResult["sqlResource"]

    # Prefer google result
    if webResult is not None:
        chosenResult = webResult["searchResult"]
        chosenResource = webResult["sqlResource"]

    if chosenResource is None:
        print "No resource saved to DB. Aborting unit creation"
        return False

    try:
        u = OPPedia(id = unit.id, name = unit.name, country = unit.country, unitClass = unit.unitClass,
                    usedResourceSearch=chosenResource,
                    rdfStoredLabel = chosenResult["label"],
                    rdfStoredResource = chosenResult["resource"])
        commit()

    except:
        print "Cannot save unit to SQL DB"
        return False

    return True


@db_session
def updateUnit(id, rdfdb):
    unit = eq.getUnit(id)

    if unit is None:
        print "Unit %d not found in game db" % id
        return False

    sqlUnit = OPPedia[id]

    if sqlUnit is None:
        return createSqlUnit(unit, rdfdb)

    print "Updating Unit %s (%d)" % (unit.getFullName(), unit.id)

    sqlRes = sqlUnit.usedResourceSearch
    foundRes = None

    if  sqlRes is not None:
        foundRes = sqlUnit.usedResourceSearch.foundResource

    if sqlUnit.forceRefresh:
        # This means that user set a custom resource URL to be loaded
        if sqlUnit.rdfStoredResource is not None and sqlUnit.rdfStoredResource != foundRes:
            print "Unit %s (%d) forced refresh" % (unit.getFullName(), id)
            if rdfdb.load(sqlUnit.rdfStoredResource):
                s = ResourceSearch(unitId = unit.id, provider = PROVIDER_CUSTOM, searchString = unit.getNicerName(), foundResource = sqlUnit.rdfStoredResource)
                sqlUnit.usedResourceSearch = s
            else:
                print "Cannot refresh PROVIDER_CUSTOM resource %s" % sqlUnit.rdfStoredResource
                return False

    # No found resource retry search and update unit if possible
    if foundRes is None and sqlRes is not None:
        print "Unit %s (%d) has a resource without search results, refreshing" % (unit.getFullName(), id)
        result = createSqlResourceSearch(id, sqlRes.searchString, rdfdb, sqlRes.provider)
        if result is not None:
            sqlUnit.rdfStoredResource = result["searchResult"]["resource"]
            sqlUnit.rdfStoredLabel = result["searchResult"]["label"]
            sqlUnit.usedResourceSearch = result["sqlResource"]
        else:
            print "Cannot refresh unit search"
            return False

    # TODO the case when unit has no google search results (to retry google)

    # Has a resource but does it have RDF data ?
    if foundRes is not None:
        if not rdfdb.hasResource(foundRes):
            print "Unit %s (%d) has a resource without rdf data, refreshing" % (unit.getFullName(), id)
            if not rdfdb.load(foundRes):
                return False

    return True


@db_session
def generateOfflineJSON(id, rdfdb, lang="en"):

    u = OPPedia[id]
    if u is None:
        print "Unit %d not found in DB" % id
        return False

    rdfResource = u.usedResourceSearch.foundResource

    if rdfResource is None:
        print "Resource for unit %d not found in RDF DB" % id
        return False

    path = os.path.join(OFFLINE_JSON_DIR, str(u.country), str(u.unitClass))

    try:
        os.makedirs(path)
    except os.error, e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            print "Cannot create complete path %s" % path
            return False


    rdfData = rdfdb.getUnitDataFromResource(rdfResource, lang)

    jsonFileName = os.path.join(path, str(u.id) + ".json")
    print "Exporting to %s " % jsonFileName

    # Fix export errors because it can't convert datatime
    def customHandler(o):
        return o.isoformat() if hasattr(o, 'isoformat') else o

    try:
        with open(jsonFileName, "w") as jsonFile:
            json.dump(rdfData, jsonFile, sort_keys=True, ensure_ascii=True, indent=4, default=customHandler)

    except Exception, e:
        print "Cannot generate json %s" % str(e)
        return False

    return True

@db_session
def offlineExportAll(rdfdb, lang="en"):
     ids = select(u.id for u in OPPedia)[:]
     for id in ids:
         generateOfflineJSON(id, rdfdb, lang)


rdfdb = OppRdf()
rdfdb.init()

for id in eq.eq:
    if updateUnit(id, rdfdb):
        time.sleep(1)


#generateOfflineJSON(79, rdfdb)
#offlineExportAll(rdfdb)
rdfdb.close()

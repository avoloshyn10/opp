#!/usr/bin/python

import openpanzer as op
from oppSql import *
from oppRdf import *
import util
from dbpedia import DbpediaQuery
from google import GoogleQuery
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
    qgoogle = GoogleQuery()

    qsearch = qdbpedia

    if provider != PROVIDER_DBPEDIA:
        qsearch = qgoogle

    r = qsearch.queryText(searchString)

    if len(r) == 0:
        print "Query %s with provider %s returned no results" % (searchString, provider)
        return None

    if provider == PROVIDER_DBPEDIA:
        rdfResource = unquote(r[0])
    else:
        rdfResource = util.wikiToDBpedia(r[0])

    # Google returned resource might be a DBpedia redirect
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
def createSqlUnit(unit, rdfdb):

    print "Creating Unit %d" % unit.id

    dbpediaSearch = util.unitNameToRegex(unit.getNicerName())
    dbpediaResult = searchRdfResource(dbpediaSearch)

    googleSearch = unit.getNicerName() + " " + unit.getClassName()
    try:
        googleResult = searchRdfResource(googleSearch, provider=PROVIDER_GOOGLE)
    except:
        print "No google results and we want them. Aborting unit creation"
        return False

    s1 = None
    s2 = None


    if dbpediaResult is not None:
        url = dbpediaResult["resource"]
        if rdfdb.load(url):
            s1 = ResourceSearch(unitId = unit.id, provider = PROVIDER_DBPEDIA, searchString = dbpediaSearch, foundResource = url)
        else:
            print "Cannot save RDF resource %s to DB" % url


    if googleResult is not None:
        url = googleResult["resource"]
        if rdfdb.load(url):
            s2 = ResourceSearch(unitId = unit.id, provider = PROVIDER_GOOGLE, searchString = googleSearch, foundResource = url)
        else:
            print "Cannot save RDF resource %s to DB" % url

    chosenResult = googleResult
    chosenResource = s2

    if s2 is None:
        chosenResult = dbpediaResult
        chosenResource = s1

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

    print "Unit %d already in DB" % id

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
    updateUnit(id, rdfdb)


#generateOfflineJSON(79, rdfdb)
#offlineExportAll(rdfdb)
rdfdb.close()

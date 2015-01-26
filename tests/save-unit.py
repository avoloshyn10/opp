def getResourcesForUnit(id):
    unit = eq.getUnit(id)

    if unit is None:
        return

    print "Looking up unit %d : %s (%s)" % (unit.id, unit.name, unit.getFullName())

    with db_session:
        o1 = OPPedia[unit.id]
        if not o1 is None:
            print "Resource already in DB updating not supported"
            return

    linkDBpedia = ""  # query will return direct link to dbpedia resource
    linkGoogle = ""  # query will return a wikipedia link
    linkGoogleSpecific = ""  # query will return a wikipedia link

    resGoogle = ""
    resGoogleSpecific = ""

    # Search strings
    dbpediaSearchString = util.unitNameToRegex(unit.getNicerName())
    googleSearchString = unit.getNicerName() + " " + unit.getClassName()
    googleSpecificSearchString = unit.getFullName()

    q = DbpediaQuery()
    qg = GoogleQuery()
    # qg.asBrowser = True

    r = q.queryText(dbpediaSearchString)
    rg = qg.queryText(googleSearchString)
    rg2 = qg.queryText(googleSpecificSearchString)

    if len(r) > 0:
        linkDBpedia = unquote(r[0])

    if len(rg) > 0:
        linkGoogle = rg[0]
        resGoogle = unquote(util.wikiToDBpedia(linkGoogle))

    if len(rg2) > 0:
        linkGoogleSpecific = rg2[0]
        resGoogleSpecific = unquote(util.wikiToDBpedia(linkGoogleSpecific))

    print "\t*DBpedia link: %s" % linkDBpedia # Won't find probably (for id 4 or other strange names)
    print "\t*Google suggested link: %s (%s)" % (resGoogle, linkGoogle) # Finds redirected resource but good one
    print "\t*Google specific suggested link: %s (%s)" % (resGoogleSpecific, linkGoogleSpecific) # Finds close resource but imo not correct

    tmp = q.getRealUri(resGoogle) # resolve dbpedia redirect
    if not tmp is None:
        resGoogle = tmp
        print "\t*Google suggested link real link: %s" % resGoogle

    # resource labels
    label1 = ""
    label2 = ""
    label3 = ""

    rdfdb = OppRdf()
    rdfdb.init()

    if linkDBpedia != "":
        print "\t -Retrieve DBpedia link"
        data1 = q.getFromResource(linkDBpedia)
        if len(data1) > 0:
            #util.dumpCommonData(data1)
            label1 = data1[0]["label"]["value"]
            print "\t >RDF DB Save DBpedia data",
            rdfdb.load(linkDBpedia)
        else:
            linkDBpedia = ""
            print "\t  ?Non-existing DBpedia page skiping"

    if resGoogle != "":
        print "\t -Retrieve Google link"
        data2 = q.getFromResource(resGoogle)
        if len(data2) > 0:
            #util.dumpCommonData(data2)
            print "\t >RDF DB Save Google data",
            label2 = data2[0]["label"]["value"]
            rdfdb.load(resGoogle)
        else:
            resGoogle = ""
            print "\t  ?Non-existing DBpedia page skiping"

    if resGoogleSpecific != "":
        print "\t -Retrieve Google Specific link"
        data3 = q.getFromResource(resGoogleSpecific)
        if len(data3) > 0:
            #util.dumpCommonData(data3)
            print "\t >RDF DB Save Google Specific data",
            label3 = data3[0]["label"]["value"]
            rdfdb.load(resGoogleSpecific)
        else:
            resGoogleSpecific = ""
            print "\t  ?Non-existing DBpedia page skiping"


    bestResource = resGoogle
    label = label2
    provider = PROVIDER_GOOGLE

    if bestResource == "":
        bestResource = resGoogleSpecific
        provider = PROVIDER_GOOGLE_SPECIFIC
        label = label3

    if bestResource == "":
        bestResource = linkDBpedia
        provider = PROVIDER_DBPEDIA
        label = label1

    if bestResource == "":
        print "Not found on DBpedia !"
        return

    with db_session:
        o1 = OPPedia[unit.id]

        if o1 is None:
            try:
                s1 = ResourceSearch(unitId = unit.id, provider = PROVIDER_DBPEDIA, searchString = dbpediaSearchString, foundResource = linkDBpedia)
                s2 = ResourceSearch(unitId = unit.id, provider = PROVIDER_GOOGLE, searchString = googleSearchString, foundResource = resGoogle)
                s3 = ResourceSearch(unitId = unit.id, provider = PROVIDER_GOOGLE_SPECIFIC, searchString = googleSpecificSearchString, foundResource = resGoogleSpecific)
                usedResource = s2
                if provider == PROVIDER_GOOGLE_SPECIFIC:
                    usedResource = s3
                elif provider == PROVIDER_DBPEDIA:
                    usedResource = s1

                o1 = OPPedia(id = unit.id, name = unit.name, country = unit.country, unitClass = unit.unitClass, usedResourceSearch=usedResource, rdfStoredLabel = label, rdfStoredResource = bestResource)
            except:
                print "Cannot save unit to SQL DB"

    rdfdb.close()
    print "Sleeping 10 seconds to not upset google"
    time.sleep(10)


if __name__ == "__main__":
    #getResourcesForUnit(484)
    #getResourcesForUnit(378)
    #getResourcesForUnit(406)
    #getResourcesForUnit(515)
    #getResourcesForUnit(521)
    #getResourcesForUnit(137)
    #getResourcesForUnit(138)
    #getResourcesForUnit(525)
    #getResourcesForUnit(536)
    #getResourcesForUnit(1769)
    #getResourcesForUnit(1860)
    #getResourcesForUnit(90)
    pass
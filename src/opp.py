#!/usr/bin/python

import openpanzer as op
from oppSql import *
import util
from sparql import SPARQLQuery
from google import GoogleQuery

import rdflib
from pprint import pprint

rdfDump = False

eq = op.Equipment()
eq.loadAllCountries()

print "Loaded %d units" % len(eq.eq)

unit = eq.getUnit(4)
text = util.unitNameToRegex(unit.name)
print "Looking up unit %s (%s)" % (unit.name, unit.getFullName())
q = SPARQLQuery()
qg = GoogleQuery()

r = q.queryText(text)
rg = qg.queryText(unit.name)
rg2 = qg.queryText(unit.getFullName())

linkDBpedia = ""
linkGoogle = None
linkGoogleSpecific = None

if len(r) > 0:
    linkDBpedia = r[0]["unit"]["value"]

if len(rg) > 0:
    linkGoogle = rg[0]

if len(rg2) > 0:
    linkGoogleSpecific = rg2[0]

print "DBpedia link: %s" % linkDBpedia # Won't find
print "Google suggested link: %s (%s)" % (util.wikiToDBpedia(linkGoogle), linkGoogle) # Finds redirected resource but good one
print "Google specific suggested link: %s (%s)" % (util.wikiToDBpedia(linkGoogleSpecific), linkGoogleSpecific) # Finds close resource but imo not correct

realResource = q.getRealUri(util.wikiToDBpedia(linkGoogle))

print "Google suggested link real link: %s" % realResource

data = q.getFromResource(util.wikiToDBpedia(linkGoogleSpecific))
util.dumpCommonData(data)

data = q.getFromResource(realResource)
util.dumpCommonData(data)

with db_session:
    s1 = ResourceSearch(unitId = unit.id, provider = PROVIDER_DBPEDIA, searchString = text, foundResource = linkDBpedia)
    s2 = ResourceSearch(unitId = unit.id, provider = PROVIDER_GOOGLE, searchString = unit.name, foundResource = util.wikiToDBpedia(linkGoogle))
    s3 = ResourceSearch(unitId = unit.id, provider = PROVIDER_GOOGLE_SPECIFIC, searchString = unit.getFullName(), foundResource = realResource)
    o1 = OPPedia(id = unit.id, name = unit.name, country = unit.country, unitClass = unit.unitClass, usedResourceSearch=s3)

if rdfDump:
    g = rdflib.Graph()
    g.parse(linkDBpedia)
    for s, p, o in g:
        print((s, p, o))


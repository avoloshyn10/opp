#!/usr/bin/python

import openpanzer as op
import util
from sparql import SPARQLQuery
from google import GoogleQuery
import rdflib
import sqlite3
import os, json, codecs, re
from pprint import pprint

fileDump = True
dbDump = False
rdfDump = False

eq = {}
for i, name in enumerate(op.countryNames):
    jsonFile = os.path.join(op.equipmentFolder, "equipment-country-" + str(i) + ".json")
    print "Loading %s for country %s (%d)" % (jsonFile, name, i)
    with open(jsonFile) as jsonData:
        j = json.load(jsonData)
        eq.update(op.unitConverter(j))

print "Loaded %d units" % len(eq)

if fileDump:
    with codecs.open("../data/unit-names.txt", "w", "utf-8") as dump:
        s = ""
        for u in eq:
            s += str(u) + " : " + eq[u].getFullName() + "\n"
        dump.write(s)

if dbDump:
    db = sqlite3.connect("../data/dbpedia-units.sqlite")
    c = db.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS units(id INTEGER PRIMARY KEY, name TEXT, country INTEGER, class INTEGER, link TEXT)
    """)
    db.commit()

    for u in eq:
        unit = eq[u]
        # text = unit.name.replace(" ", ".*?")
        # text = text.replace("(", "\\\(")
        # text = text.replace(")", "\\\)")
        text = util.unitNameToRegex(unit.name)
        print "Looking up unit %s" % unit.name
        q = SPARQLQuery()
        r = q.queryText(text)
        try:
            linkDBpedia = r[0]["unit"]["value"]
        except:
            linkDBpedia = None

        if linkDBpedia is not None:
            print "\t%s" % linkDBpedia
        else:
            print "\tNot found"

        c.execute("""
        INSERT INTO units(id, name, country, class, link) VALUES (?, ?, ?, ?, ?)
        """, (unit.id, unit.name, unit.country, unit.unitClass, linkDBpedia))
        db.commit()


unit = eq[4]
text = util.unitNameToRegex(unit.name)
print "Looking up unit %s (%s)" % (unit.name, unit.getFullName())
q = SPARQLQuery()
qg = GoogleQuery()

r = q.queryText(text)
rg = qg.queryText(unit.name)
rg2 = qg.queryText(unit.getFullName())

linkDBpedia = None
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

if rdfDump:
    g = rdflib.Graph()
    g.parse(linkDBpedia)
    for s, p, o in g:
        print((s, p, o))


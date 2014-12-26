#!/usr/bin/python

import openpanzer as op
import util
from sparql import SPARQLQuery
import rdflib
import sqlite3
import os, json, codecs, re
from pprint import pprint

fileDump = False
dbDump = False

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
            s += eq[u].getCountryName() + " " + eq[u].name + " " + eq[u].getClassName() + "\n"
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
            link = r[0]["unit"]["value"]
        except:
            link = None

        if link is not None:
            print "\t%s" % link
        else:
            print "\tNot found"

        c.execute("""
        INSERT INTO units(id, name, country, class, link) VALUES (?, ?, ?, ?, ?)
        """, (unit.id, unit.name, unit.country, unit.unitClass, link))
        db.commit()


unit = eq[135]
text = util.unitNameToRegex(unit.name)
print "Looking up unit %s" % unit.name
q = SPARQLQuery()
r = q.queryText(text)
link = r[0]["unit"]["value"]
g = rdflib.Graph()
g.parse(link)

for s, p, o in g:
    print((s, p, o))


from src import openpanzer as op
from src.sparql import SPARQLQuery
from src import util
import sqlite3
import time

eq = op.Equipment()
eq.loadAllCountries()

now = int(time.time())
db = sqlite3.connect("../data/dbpedia-units-" + str(now) + ".sqlite")
c = db.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS units(id INTEGER PRIMARY KEY, name TEXT, country INTEGER, class INTEGER, link TEXT)
""")
db.commit()

for u in eq.eq:
    unit = eq.eq[u]
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

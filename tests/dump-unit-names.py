from src import openpanzer as op
import codecs

eq = op.Equipment()
eq.loadAllCountries()

with codecs.open("../data/unit-names.txt", "w", "utf-8") as dump:
    s = ""
    for u in eq.eq:
        s += str(u) + " : " + eq.eq[u].getFullName() + "\n"
    dump.write(s)
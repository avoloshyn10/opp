from rdflib import Graph, Namespace, Literal
from rdflib.store import NO_STORE, VALID_STORE



g = Graph("Sleepycat",  identifier="openpanzer")
print "Opening RDF DB"
g.open("db", create=True)
print "Loading DBpedia 7.5_cm_Pak_40"
g.load("http://dbpedia.org/resource/7.5_cm_Pak_40")
print "Loading DBpedia 7.5_cm_Pak_97/38"
g.load("http://dbpedia.org/resource/7.5_cm_Pak_97/38")
print "Loading DBpedia Panzer_35(t)"
g.load("http://dbpedia.org/resource/Panzer_35(t)")
print "Loading DBpedia Panzer_38(t)"
g.load("http://dbpedia.org/resource/Panzer_38(t)")
print "Closing RDF DB"
g.close()

print "Opening RDF DB"
g.open("db")
print "SPARQL Results:"

for x in list(g.query(PREFIX + "SELECT ?x ?label ?abstract WHERE { ?x dbo:abstract ?abstract; rdfs:label ?label .  FILTER (LANG(?label) = 'en')  FILTER (LANG(?abstract) = 'en') }")):
    print x

g.close()
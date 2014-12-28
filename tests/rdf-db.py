from rdflib import Graph, Namespace, Literal
from rdflib.store import NO_STORE, VALID_STORE

PREFIX = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX p: <http://research.data.gov.uk/def/project/>
PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <http://dbpedia.org/ontology/>
"""

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
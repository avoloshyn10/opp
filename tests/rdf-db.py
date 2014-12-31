from src.oppRdf import *

#rdfdb = OppRdf("db")
rdfdb = OppRdf()
rdfdb.init()
print 'Triples in graph: ', len(rdfdb.g)

# print "Loading DBpedia 7.5_cm_Pak_40"
# rdfdb.load("http://dbpedia.org/resource/7.5_cm_Pak_40")
# print "Loading DBpedia 7.5_cm_Pak_97/38"
# rdfdb.load("http://dbpedia.org/resource/7.5_cm_Pak_97/38")
# print "Loading DBpedia Panzer_35(t)"
# rdfdb.load("http://dbpedia.org/resource/Panzer_35(t)")
# print "Loading DBpedia Panzer_38(t)"
# rdfdb.load("http://dbpedia.org/resource/Panzer_38(t)")
# print "Loading DBpedia Bishop artillery"
# rdfdb.load("http://dbpedia.org/resource/Bishop_(artillery)")
#print "Loading DBpedia M3_Stuart"
#rdfdb.load("http://dbpedia.org/resource/M3_Stuart")

resource = "http://dbpedia.org/resource/M4_Sherman"
j = rdfdb.getFromResource(resource)

print j["results"]["bindings"][0]["abstract"]["value"]
exit()

print "Existing data:"

query = """SELECT ?x ?label ?abstract
    WHERE {
        ?x dbo:abstract ?abstract;
        rdfs:label ?label .
        FILTER (LANG(?label) = 'en')
        FILTER (LANG(?abstract) = 'en')
    }"""

for x in list(rdfdb.g.query(OppRdf.PREFIX + query)):
    print x

print "Closing RDF DB"
rdfdb.close()
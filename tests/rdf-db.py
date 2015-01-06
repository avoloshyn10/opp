# -*- coding: utf-8 -*-
from src.oppRdf import *
from urllib import quote, unquote

import rdflib
rdfdb = OppRdf("db")
#rdfdb = OppRdf()
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

#resource = "http://dbpedia.org/resource/M4_Sherman"
resource = "http://dbpedia.org/resource/Sturmgesch%25C3%25BCtz_III"
resource = unquote(resource)
#resource = u"http://dbpedia.org/resource/Sturmgeschütz_III"
rdfdb.load(resource)


#j = rdfdb.getAllFromResource(resource)
#print j["results"]["bindings"]
rdfdb.isWeapon(resource)

#subject = rdflib.term.URIRef(resource)
#rdfdb.g.preferredLabel(subject=subject, lang='en')
#for triple in rdfdb.g.triples((subject, None, None)):
#    print triple

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
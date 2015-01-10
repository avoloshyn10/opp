# -*- coding: utf-8 -*-
from src.oppRdf import *

import rdflib
import json
from pprint import pprint

dumpData = False

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
#resource = "http://dbpedia.org/resource/M3_Stuart"

#resource = "http://dbpedia.org/resource/M4_Sherman"
resource = "http://dbpedia.org/resource/Sturmgesch%25C3%25BCtz_III"
#resource = unquote(resource)
#resource = u"http://dbpedia.org/resource/Sturmgeschütz_III"
#rdfdb.load(resource)

#rdfdb.load("http://dbpedia.org/ontology/")
#j = rdfdb.getAllFromResource(resource)
#print j["results"]["bindings"]
#rdfdb.isWeapon(resource)

oppUnitData = rdfdb.getUnitDataFromResource(resource)
pprint(oppUnitData)

#subject = rdflib.term.URIRef(u'http://dbpedia.org/ontology/weight')
#subject = rdflib.term.URIRef(resource)
#predicate = rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label')
#print rdfdb.g.preferredLabel(subject=subject, lang='en')
#for s, p, o in rdfdb.g.triples((subject, predicate, None)):
#for s, p, o in rdfdb.g.triples((None, None, None)):
#    #print s, p, o
#    if o.language == "en":
#        print o

if dumpData:
    print "Existing data:"

    # query = """SELECT ?x ?label ?abstract
    #     WHERE {
    #         ?x dbo:abstract ?abstract;
    #         rdfs:label ?label .
    #         FILTER (LANG(?label) = 'en')
    #         FILTER (LANG(?abstract) = 'en')
    #     }"""

    query = """SELECT ?x ?label
         WHERE {
             ?x rdfs:label ?label .
             FILTER (LANG(?label) = 'en')
         }"""

    for x in list(rdfdb.g.query(OppRdf.PREFIX + query)):
        print x

print "Closing RDF DB"
rdfdb.close()
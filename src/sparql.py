from SPARQLWrapper import SPARQLWrapper, JSON

class SPARQLQuery:
	def __init__(self):
		self.__sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		self.__sparql.setReturnFormat(JSON)

	def queryText(self, queryString):
		self.__sparql.setQuery("""
PREFIX dbprop: <http://dbpedia.org/property/>
PREFIX dbpont: <http://dbpedia.org/ontology/>

SELECT DISTINCT  ?unit
WHERE{
	?unit a <http://dbpedia.org/ontology/Weapon>.
	?unit rdfs:label ?label.
	?unit dbpedia-owl:abstract ?abstract.
	FILTER langMatches( lang(?label), "en" ).
	FILTER(regex(str(?abstract),"%s","i")).
}
""" % queryString)
		results = self.__sparql.query().convert()
		return results["results"]["bindings"]
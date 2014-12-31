from SPARQLWrapper import SPARQLWrapper, JSON

class DbpediaQuery:

    PREFIX = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbpprop: <http://dbpedia.org/property/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    """
    def __init__(self):
        self.__sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self.__sparql.setReturnFormat(JSON)

    def queryText(self, queryString):
        urls = []
        self.__sparql.setQuery(DbpediaQuery.PREFIX + """
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
        hits = results["results"]["bindings"]
        for h in hits:
            urls.append(h['unit']['value'])

        return urls

    def getRealUri(self, resource):
        self.__sparql.setQuery(DbpediaQuery.PREFIX + """
        SELECT ?redirect
        WHERE {
            <%s> dbpedia-owl:wikiPageRedirects ?redirect.
        }
        LIMIT 1
        """ % resource)
        results = self.__sparql.query().convert()

        uri = None
        if len(results["results"]["bindings"]) > 0:
            uri = results["results"]["bindings"][0]["redirect"]["value"]

        return uri

    def getFromResource(self, resource):
        self.__sparql.setQuery(DbpediaQuery.PREFIX + """
        SELECT DISTINCT ?label ?abstract ?thumbnail
        WHERE {
            <%s> rdfs:label ?label ;
            dbo:abstract ?abstract.
            OPTIONAL {
                <%s>  dbo:thumbnail ?thumbnail .
            }
            FILTER (LANG(?label) = 'en')
            FILTER (LANG(?abstract) = 'en')
        }
        LIMIT 1
        """ % (resource, resource))

        results = self.__sparql.query().convert()
        return results["results"]["bindings"]
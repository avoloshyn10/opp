from rdflib import Graph, Namespace, Literal
from rdflib.store import NO_STORE, VALID_STORE
import json

class OppRdf:

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

    def __init__(self, rdfFolder = "../data/oppedia-rdf"):
        self.g = Graph("Sleepycat",  identifier="openpanzer")
        self.dbName = rdfFolder

    def init(self):
        ret = self.g.open(self.dbName, create=False)

        if ret == NO_STORE:
            print "No existing database detected, creating..."
            self.g.open(self.dbName, create=True)
        else:
            assert ret == VALID_STORE, 'The underlying store is corrupt'

    def load(self, resource):
        try:
            self.g.load(resource)
            print "... OK"
        except Exception, e:
            print "... FAILED " + resource + "  " + str(e)
            return False

        return True

    def getFromResource(self, resource, lang="en"):
        r = self.g.query(OppRdf.PREFIX + """
        SELECT DISTINCT ?label ?abstract ?thumbnail
        WHERE {
            <%s> rdfs:label ?label ;
            dbo:abstract ?abstract.
            OPTIONAL {
                <%s>  dbo:thumbnail ?thumbnail .
            }
            FILTER (LANG(?label) = '%s')
            FILTER (LANG(?abstract) = '%s')
        }
        LIMIT 1
        """ % (resource, resource, lang, lang))
        return json.loads(r.serialize(format="json"))


    def close(self):
        self.g.close(commit_pending_transaction=True)


from rdflib import Graph, Namespace, Literal
from rdflib.store import NO_STORE, VALID_STORE


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
        self.g.open(self.dbName, create=True)

    def load(self, resource):
        self.g.load(resource)

    def close(self):
        self.g.close()


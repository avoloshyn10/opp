from rdflib import *
from rdflib.store import NO_STORE, VALID_STORE
from rdflib.resource import Resource
import json
from urllib import quote, unquote

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
    ONTOLOGY = "http://dbpedia.org/ontology/"

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

        if not self.hasResource(OppRdf.ONTOLOGY):
            print "OppRdf: Ontology not found loading"
            if not self.load(OppRdf.ONTOLOGY):
                print "OppRdf: Failed to load Ontology"

    def load(self, resource):
        try:
            self.g.load(unquote(resource))
            print "... OK"
        except Exception, e:
            print "... FAILED " + resource + "  " + str(e)
            return False

        return True

    def isResource(self, o):
        return isinstance(o, Resource)

    def isLiteral(self, o):
        return isinstance(o, Literal)

    def isWeapon(self, resource):
        uri = URIRef(resource)
        weapon = URIRef('http://dbpedia.org/ontology/Weapon')
        ret = self.g.query("ASK {?uri a ?weapon}", initBindings={'uri': uri, 'weapon': weapon})
        print uri, "is a weapon?", ret.askAnswer
        return ret.askAnswer

    def hasResource(self, resource):
        uri = URIRef(resource)
        return (uri, None, None) in self.g

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
        return json.loads(r.serialize(format="json")) #TODO: Maybe serialize('python')

    def getAllFromResource(self, resource, lang="en"): #TODO: Needs rewrite as it doesn't list properties that don't have a label language like sameAs
        r = self.g.query(OppRdf.PREFIX + """
        SELECT ?p ?o
        WHERE {
            <%s> ?p ?o .
        }
        """ % (resource))
        #FILTER(langMatches(lang(?o), "en") or LANG(?o) = "") #TODO: Filter breaks rdflib parsing
        return json.loads(r.serialize(format="json"))

    def getUnitDataFromResource(self, resource, lang="en"):
        u = URIRef(unquote(resource))
        r = self.g.resource(u)

        oppUnitData = {}

        for p, o in r.predicate_objects():
            try:
                keyName = p.qname().split(":")[1]
                name = keyName
                value = None
                #TODO move to a dictionary
                if keyName == "sameAs" or keyName == "comment" or keyName == "type" or "wiki" in keyName:
                    continue

                if keyName == "wasDerivedFrom" or keyName == "hasPhotoCollection" or keyName == "caption" or keyName == "depiction":
                    continue

                if keyName == "wordnet_type" or keyName == "isPrimaryTopicOf" or keyName == "subject":
                    continue

                if self.isResource(p) and self.hasResource(p):
                    rr = self.g.resource(p)
                    #name = p.value(RDFS.label) # There are multiple lables might return some other language
                    name = self.g.preferredLabel(subject=URIRef(p), lang='en')[0][1].toPython()

                if self.isLiteral(o):
                    if o.language is None or o.language == "en" or o.language == "":
                        value = o.toPython()
                    #else:
                    #    print "lang = " + o.language
                elif self.isResource(o):
                    value = URIRef(o).toPython()
                else:
                    value = o.qname()

                if value is not None and keyName is not None:
                    tmp = oppUnitData.get(keyName, None)
                    if tmp is not None:
                        tmp["values"].append(value)
                    else:
                        tmp = {}
                        tmp["name"] = name
                        tmp["values"] = [value]

                    oppUnitData[keyName] = tmp

            except Exception, e:
                print "Error " + str(e)
                pass

        return oppUnitData

    def close(self):
        self.g.close(commit_pending_transaction=True)


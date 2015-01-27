from datetime import datetime
from pony.converting import str2datetime
from pony.orm import *

db = Database("sqlite", "../data/oppedia.sqlite", create_db=True)

PROVIDER_DBPEDIA = "DBPEDIA"
PROVIDER_GOOGLE = "GOOGLE"
PROVIDER_GOOGLE_SPECIFIC = "GOOGLE SPECIFIC"
PROVIDER_CUSTOM = "CUSTOM"
PROVIDER_BING = "BING"

class ResourceSearch(db.Entity):
    id = PrimaryKey(int, auto=True)
    unitId = Required(int)
    provider = Required(str)
    searchString = Required(str)
    foundResource = Optional(str)
    performed = Optional(datetime)
    oppediaUnit = Optional("OPPedia")

class OPPedia(db.Entity):
    id = PrimaryKey(int, auto=True) #TODO we actually want unit id from openpanzer unit json "db"
    name = Required(unicode)
    country = Required(int)
    unitClass = Required(int)
    rdfStoredLabel = Optional(unicode)
    rdfStoredResource = Optional(str)
    forceRefresh = Required(bool, default=False)
    usedResourceSearch = Optional(ResourceSearch)

sql_debug(False)

db.generate_mapping(create_tables=True)






from bottle import default_app, install, route, request, redirect, run, template, static_file, view, TEMPLATE_PATH
from pony.orm.integration.bottle_plugin import PonyPlugin
from oppSql import *
import openpanzer as op
from util import *
from oppRdf import *
from threading import Thread
import restWorkThread as wt
import opp

TEMPLATE_PATH.insert(0,'../restclient/templates/')

rdfdb = OppRdf()
rdfdb.init()

install(PonyPlugin())

eq = op.Equipment()
#eq.loadAllCountries()

eq.loadCountry(8) # Germany

gameUnits = eq.eq

# Fix export errors because it can't convert datetime
def customHandler(o):
    return o.isoformat() if hasattr(o, 'isoformat') else o


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='../restclient/')

@route('/')
@route('/units/')
@view('all_units')
def all_units():
    units = select(u.id for u in OPPedia)[:] # Get a list of id
    for id in gameUnits:
        gameUnit = gameUnits[id]
        gameUnits[id].processed = False
        if id in units:
            gameUnits[id].processed = True

    return  dict(units=units, gameUnits=gameUnits)

@route('/units/:id/')
@view('show_unit')
def show_unit(id):
    u = OPPedia[id]
    if u is None:
        return edit_unit(id)

    searches = select( s for s in ResourceSearch if s.unitId == id)
    unit = op.Unit(id, name=u.name, country=u.country, unitClass=u.unitClass)
    rdfdata = rdfdb.getFromResource(u.usedResourceSearch.foundResource)
    try:
        thumbnail = rdfdata["results"]["bindings"][0]["thumbnail"]["value"]
        abstract = rdfdata["results"]["bindings"][0]["abstract"]["value"]
    except:
        thumbnail = ""
        abstract = "Abstract Not found on RDF DB"

    return dict(u=u, unit=unit, searches=searches, unquoteUrl=unquoteUrl, thumbnail=thumbnail, abstract=abstract)


@route('/units/:id/details/')
@view('show_unit_details')
def show_unit_details(id):
    u = OPPedia[id]
    if u is None:
        return edit_unit(id)

    unit = op.Unit(id, name=u.name, country=u.country, unitClass=u.unitClass)
    rdfdata = json.dumps(rdfdb.getUnitDataFromResource(u.usedResourceSearch.foundResource), ensure_ascii=True, default=customHandler)

    return dict(u=u, unit=unit,  unquoteUrl=unquoteUrl, rdfdata=rdfdata)

@route('/units/:id/rdf/')
@view('show_unit_rdf')
def show_unit_rdf(id):
    u = OPPedia[id]
    if u is None:
        return edit_unit(id)

    unit = op.Unit(id, name=u.name, country=u.country, unitClass=u.unitClass)
    rdfdata = json.dumps(rdfdb.getAllFromResource(u.usedResourceSearch.foundResource), ensure_ascii=True, default=customHandler)

    return dict(u=u, unit=unit,  unquoteUrl=unquoteUrl, rdfdata=rdfdata)

@route('/units/:id/edit/')
@view('edit_unit')
def edit_unit(id):
    u = OPPedia[id]
    if u is None:
        u = gameUnits[int(id)]

    searches = select( s for s in ResourceSearch if s.unitId == id)
    return dict(u=u, searches=searches)

@route('/units/:id/edit/', method='POST')
def save_unit(id):
    modified = False
    u = OPPedia[id]
    forceRefresh = request.forms.get('forceRefresh') or False
    if forceRefresh:
        modified = True
        u.forceRefresh = forceRefresh
    rdfStoredResource = request.forms.get('resourceCreate')
    if len(rdfStoredResource) > 0 and u.rdfStoredResource != rdfStoredResource:
        modified = True
        u.rdfStoredResource = rdfStoredResource
        u.forceRefresh = True
    else:
        rdfStoredResource = None # unitUpdate tests for None
    querySelect = int(request.forms.get('querySelect'))
    if querySelect != u.usedResourceSearch.id:
        modified = True
        u.usedResourceSearch = get(s for s in ResourceSearch if s.unitId == id and s.id == querySelect)
        commit()
    if u.forceRefresh:
        wt.reqs.put((opp.updateUnit, (u.id, rdfdb), {'eqlist': eq}))
    redirect("/units/%d/" % u.id)

@route('/test/addtoqueue', method='GET')
def add_to_queue():
    # This doesn't work any more
    wt.reqs.put((wt.REQ_NONE, None, None, None))
    return """
        <html><body>Added to queue</body></html>
    """

worker = Thread(name = "spider thread", target = wt.work, args = (eq, rdfdb))
worker.daemon = True # Die with main thread
worker.start()

run(debug=True, host='localhost', port=8080, reloader=False)
rdfdb.close()

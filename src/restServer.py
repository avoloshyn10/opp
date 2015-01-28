from bottle import default_app, install, route, request, redirect, run, template, static_file
from pony.orm.integration.bottle_plugin import PonyPlugin
from oppSql import *
import openpanzer as op
from util import *
from oppRdf import *
from threading import Thread
import restWorkThread as wt


rdfdb = OppRdf()
rdfdb.init()

install(PonyPlugin())

eq = op.Equipment()
#eq.loadAllCountries()


eq.loadCountry(8) # Germany

gameUnits = eq.eq

# Fix export errors because it can't convert datatime
def customHandler(o):
    return o.isoformat() if hasattr(o, 'isoformat') else o

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='../restclient/')

@route('/')
@route('/units/')
def all_units():
    units = select(u.id for u in OPPedia)[:] # Get a list of id
    for id in gameUnits:
        gameUnit = gameUnits[id]
        gameUnits[id].processed = False
        if id in units:
            gameUnits[id].processed = True

#    %for u in units:
#        <li><a href="/units/{{ u.id }}/">{{ u.name }}</a></li>
#    %end

    return template('''
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
    </head>
    <body>
    <h1>List of units</h1>
    <table class="table">
    <thead>
    <tr>
        <th> # </th>
        <th> Name </th>
        <th> Country </th>
        <th> Class </th>
        <th> Queried </th>
    </tr>
    </thead>
    <tbody>
    %for id in gameUnits:
        %u = gameUnits[id]
        <tr>
        <th> {{ u.id }} </th>
        <td> <a href="/units/{{ u.id }}/">{{ u.name }}</a></td>
        <td> {{u.getCountryName()}} ({{u.country}}) </td>
        <td> {{u.getClassName()}} ({{u.unitClass}})</td>
        %if u.processed :
            <td><a href="/units/{{u.id}}/edit/" role="button" class="btn btn-success">Yes</a></td>
        %else:
            <td><a href="/units/{{u.id}}/edit/" role="button" class="btn btn-danger">No </a></td>
        %end
         </tr>
    %end
    </tbody>
    </table>
    </body>
    </html>
    ''', units=units, gameUnits=gameUnits)

@route('/units/:id/')
def show_unit(id):

    u = OPPedia[id]
    searches = select( s for s in ResourceSearch if s.unitId == id)
    unit = op.Unit(id, name=u.name, country=u.country, unitClass=u.unitClass)
    rdfdata = rdfdb.getFromResource(u.usedResourceSearch.foundResource)
    try:
        thumbnail = rdfdata["results"]["bindings"][0]["thumbnail"]["value"]
        abstract = rdfdata["results"]["bindings"][0]["abstract"]["value"]
    except:
        thumbnail = ""
        abstract = "Abstract Not found on RDF DB"

    return template('''
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
    </head>
    <body>
    <div class="container">
    <h1>{{ u.name }}  <small>{{unit.getCountryName()}} ({{u.country}}) {{unit.getClassName()}} ({{u.unitClass}})</small></h1>
    <br>
    <div class="thumbnail">
        <img class="img-resposive" src='{{ thumbnail }}'>
        <div class="caption">
        <p>{{ abstract }}</p>
        </div>
    </div>

    <p>RDF Resource: <a href="{{ unquoteUrl(u.usedResourceSearch.foundResource)}}">{{ unquoteUrl(u.usedResourceSearch.foundResource)}}</a></p>
    <p>RDF Resource found with: {{ u.usedResourceSearch.provider}}</p>
    <p>Query text:  {{ u.usedResourceSearch.searchString }}</p>
    <p>Stored RDF label: {{ u.rdfStoredLabel }}</p>
    <p>Stored RDF resource: {{ u.rdfStoredResource }} </p>
    <p>Queries for this unit:</>
    <ul>
        %for s in searches:
            <li>{{s.searchString }} -  {{ s.provider}} - <a href="{{ s.foundResource}}">{{ s.foundResource}}</a></li>
        %end
    </ul>


    <br>

    <a href="/units/{{ u.id }}/details/" role="button" class="btn btn-primary">Unit Details</a>
    <a href="/units/{{ u.id }}/rdf/" role="button" class="btn btn-primary">Show RDF data</a>
    <a href="/units/{{ u.id }}/edit/" role="button" class="btn btn-primary">Edit unit resource</a>
    <a href="/units/" role="button" class="btn btn-primary">Return to all units</a>
    </div>
    </body>
    </html>
    ''', u=u, unit=unit, searches=searches, unquoteUrl=unquoteUrl, thumbnail=thumbnail, abstract=abstract)

@route('/units/:id/details/')
def show_unit_details(id):

    u = OPPedia[id]
    unit = op.Unit(id, name=u.name, country=u.country, unitClass=u.unitClass)
    rdfdata = json.dumps(rdfdb.getUnitDataFromResource(u.usedResourceSearch.foundResource), ensure_ascii=True, default=customHandler)

    return template('''
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
    </head>
    <body>
    <script language="javascript">

    function printUnitData(parsedJson, tableId, tableClassName, linkText)
    {
        var div = document.getElementById("dataContainer");
        for (var key in parsedJson)
        {
            var info = parsedJson[key];
            var name = info["name"];
            var value = info["values"];
            //var news = document.getElementsByClassName("news-story")[0];

            div.innerHTML += "<dt>" + name + "</dt><dd> " + value + "</dd>";
            //container.appendChild(div);
        }

    }
    </script>
    <div class="container">
    <h1>{{ u.name }}  <small>{{unit.getCountryName()}} ({{u.country}}) {{unit.getClassName()}} ({{u.unitClass}})</small></h1>
    <p><a href="{{ unquoteUrl(u.usedResourceSearch.foundResource)}}">{{ unquoteUrl(u.usedResourceSearch.foundResource)}}</a> (Provider {{ u.usedResourceSearch.provider}})</p>
    <dl class="dl-horizontal" id="dataContainer">
    <script>printUnitData({{!rdfdata}}, "unitDataTable", null, "Link")</script>
    </dl>

    <br>
    <a href="/units/{{ u.id }}/edit/" role="button" class="btn btn-primary">Edit unit resource</a>
    <a href="/units/{{ u.id }}/" role="button" class="btn btn-primary">Back to unit</a>
    <a href="/units/" role="button" class="btn btn-primary">Return to all units</a>
    </div>
    </body>
    </html>
    ''', u=u, unit=unit,  unquoteUrl=unquoteUrl, rdfdata=rdfdata)

@route('/units/:id/rdf/')
def show_unit_rdf(id):

    u = OPPedia[id]

    if u is None:
        return edit_unit(id)

    unit = op.Unit(id, name=u.name, country=u.country, unitClass=u.unitClass)
    rdfdata = json.dumps(rdfdb.getAllFromResource(u.usedResourceSearch.foundResource), ensure_ascii=True, default=customHandler)

    return template('''
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
    </head>
    <body>
    <script language="javascript">
    function output(inp) {
        document.body.appendChild(document.createElement('pre')).innerHTML = inp;
    }
    function prettyPrint(json) {
    if (typeof json != 'string') {
         json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
    }
    </script>
    <div class="container-fluid">
    <h1>{{ u.name }}</h1>
    <p>Country: {{ u.country }} - {{ unit.getCountryName() }}</p>
    <p>Class: {{ u.unitClass }} - {{ unit.getClassName() }}</p>
    <p>RDF Resource: <a href="{{ unquoteUrl(u.usedResourceSearch.foundResource)}}">{{ unquoteUrl(u.usedResourceSearch.foundResource)}}</a></p>
    <p>RDF Resource found with: {{ u.usedResourceSearch.provider}}</p>
    <script>output(prettyPrint({{!rdfdata}}))</script>
    <br>
    <a href="/units/{{ u.id }}/edit/" role="button" class="btn btn-primary">Edit unit resource</a>
    <a href="/units/{{ u.id }}/" role="button" class="btn btn-primary">Back to unit</a>
    <a href="/units/" role="button" class="btn btn-primary">Return to all units</a>
    <br>
    </div>
    </body>
    </html>
    ''', u=u, unit=unit,  unquoteUrl=unquoteUrl, rdfdata=rdfdata)

@route('/units/:id/edit/')
def edit_unit(id):
    u = OPPedia[id]

    if u is None:
        u = gameUnits[int(id)]

    searches = select( s for s in ResourceSearch if s.unitId == id)
    return template('''
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
    </head>
    <body>
    <div class="container">
    <h1> Edit Unit Resource Query</h1>
    <form action='/units/{{ u.id }}/edit/' method='post'>
        <div class="form-group">
        <label for="unitName">Unit Name</label>
        <input id="unitName" class="form-control" type="text" value="{{u.name}}" disabled>
        <label for="querySelect">Select Existing Query</label><br>
        <select id="querySelect" name="querySelect">
            %for s in searches:
                <option value="{{s.id}}">{{ s.foundResource}}</option>
            %end
        </select>
        <br><b>or</b><br>
        <label for="resourceCreate">Add and Select a new resource</label>
        <input id="resourceCreate" name="resourceCreate" class="form-control" type="text" placeHolder="dbpedia.org url">
        <p class="help-block">If filled it will set the unit resource to corresponding URL and retrieve new RDF data </p>

        <label><input type="checkbox" name="forceRefresh" id="forceRefresh" checked> Force RDF data refresh</label>
        </div>
        <button type="submit" class="btn btn-success">Save </button>
        <a href="/units/{{ u.id }}/" role="button" class="btn btn-primary">Back to unit</a>
        <a href="/units/" role="button" class="btn btn-primary">Return to all units</a>
    </form>
    </div>
    </body>
    </html>
    ''', u=u, searches=searches)

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
        wt.reqs.put((wt.REQ_UPDATE_UNIT, u, rdfdb, eq)) # TUPLE!
    redirect("/units/%d/" % u.id)

@route('/test/addtoqueue', method='GET')
def add_to_queue():
    wt.reqs.put((wt.REQ_NONE, None, None, None))
    return """
        <html><body>Cucu</body></html>
    """

worker = Thread(None, wt.work, (), {})
worker.daemon = True # Die with main thread
worker.start()

run(debug=True, host='localhost', port=8080, reloader=False)
rdfdb.close()

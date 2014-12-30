from bottle import default_app, install, route, request, redirect, run, template
from pony.orm.integration.bottle_plugin import PonyPlugin
from oppSql import *
import openpanzer as op
from util import *

install(PonyPlugin())

@route('/')
@route('/units/')
def all_units():
    units = select(u for u in OPPedia)
    return template('''
    <h1>List of units</h1>
    <ul>
    %for u in units:
        <li><a href="/units/{{ u.id }}/">{{ u.name }}</a>
    %end
    </ul>
    ''', units=units)

@route('/units/:id/')
def show_unit(id):

    u = OPPedia[id]
    searches = select( s for s in ResourceSearch if s.unitId == id)
    unit = op.Unit(id, name=u.name, country=u.country, unitClass=u.unitClass)

    return template('''
    <h1>{{ u.name }}</h1>
    <p>Country: {{ u.country }} - {{ unit.getCountryName() }}</p>
    <p>Class: {{ u.unitClass }} - {{ unit.getClassName() }}</p>
    <p>RDF Resource: <a href="{{ unquoteUrl(u.usedResourceSearch.foundResource)}}">{{ unquoteUrl(u.usedResourceSearch.foundResource)}}</a></p>
    <p>RDF Resource found with: {{ u.usedResourceSearch.provider}}</p>
    <p>Query text:  {{ u.usedResourceSearch.searchString }}</p>
    <p>Stored RDF label: {{ u.rdfStoredLabel }}</p>
    <p>Stored RDF resource: {{ u.rdfStoredResource }} </p>
    <br>
    <p>Other queries for this unit:</>
    <ul>
        %for s in searches:
            <li>{{s.searchString }} -  {{ s.provider}} - <a href="{{ s.foundResource}}">{{ s.foundResource}}</a></li>
        %end
    </ul>


    <br>
    <a href="/units/{{ u.id }}/edit/">Edit unit resource</a>
    <a href="/units/">Return to all units</a>
    ''', u=u, unit=unit, searches=searches, unquoteUrl=unquoteUrl)

@route('/units/:id/edit/')
def edit_units(id):
    u = OPPedia[id]
    return template('''
    <form action='/units/{{ u.id }}/edit/' method='post'>
      <table>
        <tr>
          <td>Unit name:</td>
          <td>{{ u.name }}</td>
        </tr>
        <tr>
          <td>Force RDF data refresh</td>
          <td><input type="checkbox" name="forceRefresh">
        </tr>
      </table>
      <input type="submit" value="Save!">
    </form>
    <p><a href="/units/{{ u.id }}/">Discard changes</a>
    <p><a href="/units/">Return to all units</a>
    ''', u=u)

@route('/units/:id/edit/', method='POST')
def save_unit(id):
    u = OPPedia[id]
    u.forceRefresh = request.forms.get("forceRefresh")
    redirect("/units/%d/" % u.id)

run(debug=True, host='localhost', port=8080, reloader=True)

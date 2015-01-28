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
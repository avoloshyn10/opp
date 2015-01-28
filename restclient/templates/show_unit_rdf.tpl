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
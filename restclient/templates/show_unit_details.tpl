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
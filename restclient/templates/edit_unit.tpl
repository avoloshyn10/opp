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
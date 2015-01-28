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
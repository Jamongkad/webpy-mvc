<html>
    <head> 
        <script type="text/javascript" src="/static/js/jquery.js"></script>
        <script type="text/javascript" src="/static/js/underscore-min.js"></script>   
        <script type="text/javascript" src="/static/js/jquery.asmselect.js"></script>   
        
        <link rel="stylesheet" type="text/css" href="/static/css/reset.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/fluid_grid.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/jquery.asmselect.css"></link>

        <link rel="stylesheet" type="text/css" href="/static/css/sunguppy_1.2.css"></link>
        <title>${self.title()}</title>

    </head>
    <body>
    <%! import header %>
    ${header.index().GET()}
    <div class="container_12"> 
        ${self.body()}  
    </div>
    </body>
</html>

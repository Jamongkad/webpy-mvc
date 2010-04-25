<html>
    <head> 
        <script type="text/javascript" src="/static/js/jquery.js"></script>
        <script type="text/javascript" src="/static/js/underscore-min.js"></script>   
        <link rel="stylesheet" type="text/css" href="/static/css/reset.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/fluid_grid.css"></link>
        <title>${self.title()}</title>
    </head>
    <body>
    <div class="container_12">
        <div class="grid_12">Header</div>
        ${self.body()} 
        <div class="grid_12"> Footer</div>
    </div>
    </body>
</html>

import app_globals
import web

from view import render

urls = (
    '/(.*)', 'index'
)

class index(object):
    def GET(self, name):
        return render('welcome.mako', name=name)

app = web.application(urls, globals())

#!/usr/bin/env python
import app_globals
import web

from view import render

import welcome

urls = (
    '/', 'index',
    '/maro/(.*)', 'maro',
    '/test', 'testing',
    '/welcome', welcome.app
)

app = web.application(urls, globals(), autoreload=True)

class index(object):
    def GET(self):
        return render('test.mako')

class testing(object):
    def GET(self):
        gets = web.input()
        return gets

class maro(object):
    def GET(self, name):
        return welcome.index().GET(name)

if __name__ == "__main__":
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()

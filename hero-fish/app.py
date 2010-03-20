#!/usr/bin/env python
import web
import app_globals

from view import render
from auth import session, User
from pymongo import Connection

import welcome

web.config.debug = True

urls = (
    '/', 'index',
    '/maro/(.*)', 'maro',
    '/test', 'testing',
    '/test_session', 'test_session',
    '/session_active', 'session_active',
    '/login', 'login',
    '/logout', 'logout',
    '/welcome', welcome.app
)

db = Connection().sprocket_db
app = web.application(urls, globals(), autoreload=True)

from SprocketAuth import SprocketAuth
SprocketAuth(app)

class index(object):
    def GET(self):
        return render('test.mako')

class session_active(object):
    def GET(self): 
        if web.ctx.session.get('loggedIn') is True:
            return 'You are here cuz session is active'
        return web.seeother(web.ctx.homedomain)

class test_session(object):
    def GET(self):
        return web.ctx.env

class logout(object):
    def GET(self):
        web.ctx.session.loggedIn = False

class login(object):
    def GET(self):
        web.ctx.session.loggedIn = True

class testing(object):
    def GET(self):
        get = web.input()
        query = session.query(User).filter_by(name=get.name).first()
        mongo_query = db.users.find_one({'name' : get.name}) 
        return mongo_query

class maro(object):
    def GET(self, name):
        return welcome.index().GET(name)

if __name__ == "__main__":
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()

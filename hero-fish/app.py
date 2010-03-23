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
sa = SprocketAuth(app)

class index(object):
    def GET(self):
        return render('test.mako')
        
class session_active(object):
    @sa.protect()
    def GET(self):   
        return 'pwet'
       
class test_session(object):
    @sa.protect()
    def GET(self):
        return 'mathew'

class logout(object):
    def GET(self):
        sa.logout()

class login(object):
    def POST(self):
        post = web.input()
        import hashlib
        password = hashlib.sha1(post.password).hexdigest()
        mongo_query = db.users.find_one({'name' : post.user_name, 'password' : password}) 
        return sa.login({ 
            'check' : mongo_query,
            'redirect_to_if_pass' : '../session_active',
        })

class testing(object):
    def GET(self):
        get = web.input()
        #query = session.query(User).filter_by(name=get.name).first() 
        import hashlib
        password = hashlib.sha1(get.password).hexdigest()
        mongo_query = db.users.find_one({'name' : get.name, 'password' : password}) 

        if mongo_query:
            return 'matched'
        return 'no match'

class maro(object):
    def GET(self, name):
        return welcome.index().GET(name)

if __name__ == "__main__":
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()

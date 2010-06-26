#!/usr/bin/env python
import web
import app_globals

from view import render
from auth import session, User
from pymongo import Connection

from forms import LoginAccountForm, CreateAccountForm
from myrequest import Request
from SprocketAuth import SprocketAuth

import welcome, catalog, masthead, header

web.config.debug = True

urls = (
    '/', 'index',
    '/maro/(.*)', 'maro',
    '/login', 'login',
    '/logout', 'logout',
    '/create_account', 'create_account',
    '/welcome', welcome.app,
    '/catalog', catalog.app,
)

db = Connection().sprocket_db
app = web.application(urls, globals(), autoreload=True)
 

sa = SprocketAuth(app)

class index(object):
    def GET(self):
        products = db.catalog
        return render('index.mako', products=products)

class create_account(object):
    @sa.protect()
    def GET(self): pass

    def POST(self): 
        login  = LoginAccountForm()
        create = CreateAccountForm(Request().POST) 
        if create.validate() != True:
            return render('index.mako', login=login, create=create)
        return web.input()
 
class logout(object):
    def GET(self):
        sa.logout()
        return web.seeother('../')

class login(object):
    def POST(self):
        login  = LoginAccountForm(Request().POST)
        create = CreateAccountForm() 
        if login.validate() != True:
            return render('index.mako', login=login, create=create)

        post = web.input()
        import hashlib
        password = hashlib.sha1(post.password).hexdigest()
        mongo_query = db.users.find_one({'name' : post.username, 'password' : password}) 

        if mongo_query:
            user = mongo_query['_id']
        else:
            user = False

        return sa.login({ 
            'check' : mongo_query,
            'redirect_to_if_pass' : '../welcome/',
            'redirect_to_if_fail' : '../',
            'user' : user
        })

class maro(object):
    def GET(self, name):
        return masthead.index().GET()

if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()

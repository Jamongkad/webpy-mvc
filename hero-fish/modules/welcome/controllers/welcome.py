import app_globals
import web

from pymongo import Connection
from view import render
from forms import CreateAccountForm
from webob import Request

db = Connection().sprocket_db

urls = (
    '/', 'index',
    '/select', 'select',
    '/create_account', 'create_account'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    @sa.protect()
    def GET(self): 
        request = web.input()
        frm = CreateAccountForm()
        return render('welcome.mako', frm=frm)

class create_account(object):
    @sa.protect()
    def GET(self):
        pass

    def POST(self):
        input = web.data()
        env = web.ctx.env
        request = Request(env)
        request.method = 'POST'
        request.body = input
        frm = CreateAccountForm(request.POST) 
        if frm.validate() != True:
            return render('welcome.mako', frm=frm)
        return 'pass create account bzzt!'
 
class select(object):
    @sa.protect()
    def GET(self):
        input = web.input()
        result = db.units.find_one({'name' : input.name})
        return result



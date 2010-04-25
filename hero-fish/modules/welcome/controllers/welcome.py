import app_globals
import web

from pymongo import Connection
from view import render
from forms import CreateAccountForm

db = Connection().sprocket_db

urls = (
    '/', 'index',
    '/select', 'select'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    @sa.protect()
    def GET(self): 
        frm = CreateAccountForm()
        return render('welcome.mako', frm=frm)

class select(object):
    @sa.protect()
    def GET(self):
        input = web.input()
        result = db.units.find_one({'name' : input.name})
        return result



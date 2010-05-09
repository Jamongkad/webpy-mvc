import app_globals
import web

from pymongo import Connection
from view import render
from forms import ChooseOccup
from myrequest import Request

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
        occup = ChooseOccup()
        return render('welcome.mako', occup=occup)

class create_account(object):
    @sa.protect()
    def GET(self):
        pass

    def POST(self):
        frm = CreateAccountForm(Request().POST) 
        if frm.validate() != True:
            return render('welcome.mako', frm=frm)
        return web.input()
 
class select(object):
    @sa.protect()
    def GET(self):
        input = web.input()
        result = db.units.find_one({'name' : input.name})
        return result



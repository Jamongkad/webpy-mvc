import app_globals
import web

from pymongo import Connection
from view import render
from forms import ChooseOccup
from myrequest import Request

db = Connection().sprocket_db

urls = (
    '/', 'index',
    '/add_info', 'add_info',
    '/create_account', 'create_account'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    @sa.protect()
    def GET(self): 
        planets = db.planets.find()
        user_id = web.ctx.session['user_id']
        return render('welcome.mako', planets=planets, user_id=user_id)

class add_info(object):
    def POST(self):
        from pymongo.objectid import ObjectId
        i = web.input(planets=[])
        usr = db.users.find_one({'_id': ObjectId(i['user_id'])})

        usr['planets_owned'] = i['planets']
        db.users.save(usr)
        return "saved!"

        

class create_account(object):
    @sa.protect()
    def GET(self):
        pass

    def POST(self):
        frm = CreateAccountForm(Request().POST) 
        if frm.validate() != True:
            return render('welcome.mako', frm=frm)
        return web.input() 

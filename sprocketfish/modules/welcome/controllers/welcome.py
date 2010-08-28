import app_globals
import web

from sqlalchemy.ext.sqlsoup import SqlSoup
from view import render
from forms import ChooseOccup

urls = (
    '/', 'index',
    '/add_info', 'add_info',
    '/create_account', 'create_account'
)

db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    @sa.protect()
    def GET(self):   
        user_id = web.ctx.session.user_id
        name = db.users.filter_by(id=user_id).first().name
        return render('welcome.mako', name=name)

      
class add_info(object):
    def POST(self):
        i = web.input(planets=[])
        planets = i['planets']
        if not planets:
            return "no planets"
        else:
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

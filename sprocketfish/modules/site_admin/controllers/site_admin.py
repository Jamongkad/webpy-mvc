import app_globals
import web

from pymongo import Connection
from pymongo.objectid import ObjectId
from view import render
from forms import ChooseOccup
from myrequest import Request

db = Connection().sprocket_db

urls = (
    '/(.*)', 'index'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    def GET(self, site_type):  
        return site_type

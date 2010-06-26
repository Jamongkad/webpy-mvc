import app_globals
import web

from pymongo import Connection
from pymongo.objectid import ObjectId
from view import render
from myrequest import Request
from forms import LoginAccountForm, CreateAccountForm
import masthead

urls = (
    '/', 'index',
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    def GET(self):
        return render('header.mako', login=LoginAccountForm(), create=CreateAccountForm(), masthead=masthead.index().GET('Mathew'))

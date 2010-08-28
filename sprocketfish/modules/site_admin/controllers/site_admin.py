#!/usr/bin/env python
import app_globals
import web

from view import render
from forms import ChooseOccup
from myrequest import Request

from sqlalchemy.ext.sqlsoup import SqlSoup
from forms import LoginAccountForm, CreateAccountForm

urls = (
    '/sa/(.*)', 'index',
    '/login_user', 'login_user',
    '/create_account', 'create_account',
    '/logout', 'logout'
)

app = web.application(urls, globals())
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)

class index(object):
    def GET(self, site_type):  
        login = LoginAccountForm()
        create = CreateAccountForm()
        return render('site_admin.mako', site_type=site_type, login=login, create=create)

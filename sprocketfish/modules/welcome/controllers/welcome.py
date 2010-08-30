import app_globals
import web

from sqlalchemy.ext.sqlsoup import SqlSoup
from view import render
from forms import AddJob
from db import User, Job, session

urls = (
    '/', 'index',
    '/add_job', 'add_job',
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
        jobs = db.jobs.all()
        job_form = AddJob()  
        return render('welcome.mako', name=name, jobs=jobs, job_form=job_form)

      
class add_job(object):
    def POST(self):
        i = web.input()
        db.jobs.insert(job_nm=i.job_name, job_desc=i.job_desc)
        db.commit()
        web.redirect('../welcome/')

class create_account(object):
    @sa.protect()
    def GET(self):
        pass

    def POST(self):
        frm = CreateAccountForm(Request().POST) 
        if frm.validate() != True:
            return render('welcome.mako', frm=frm)
        return web.input() 

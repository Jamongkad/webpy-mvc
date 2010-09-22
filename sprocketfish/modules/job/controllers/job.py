import app_globals
import web

from sqlalchemy import or_, and_, desc
from view import render
from forms import AddJob
from db import User, Job, session, sql_db as db
from myrequest import Request

from mx.DateTime import DateTime

urls = (
    '/', 'index',
    '/view/(.*)', 'view'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class view(object):
    @sa.protect()
    def GET(self, job_id):    
        return db.jobs.filter_by(job_id=job_id).first()

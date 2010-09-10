import app_globals
import web

from sqlalchemy.ext.sqlsoup import SqlSoup
from sqlalchemy import or_, and_, desc
from view import render
from forms import AddJob
from db import User, Job, session
from myrequest import Request

from mx.DateTime import DateTime

urls = (
    '/', 'index',
    '/view/(.*)', 'view'
)

try:
    db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)
except:
    db.rollback()
    raise

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)


class view(object):
    @sa.protect()
    def GET(self, job_id):   
        return db.jobs.filter_by(job_id=job_id).first()

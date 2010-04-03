import web

class SprocketAuth(object):

    def __init__(self, app):
        self.session = web.session.Session(app, web.session.DiskStore('sessions'))

        def session_hook():
            web.ctx.session = self.session

        app.add_processor(web.loadhook(session_hook))

    def protect(self, redirect=False): 
        def meth_signature(meth):
            def new(*args, **kwa):
                if web.ctx.session.get('loggedIn') is True:
                    return meth(*args, **kwa)
                if redirect is False:
                    raise web.seeother(web.ctx.homedomain) 
                raise web.seeother(redirect)
            return new
        return meth_signature

    def login(self, login_vars):  
        if login_vars.get('check'):
            web.ctx.session.loggedIn = True
            if login_vars.get('redirect_to_if_pass'):
                raise web.seeother(login_vars.get('redirect_to_if_pass'))
            else:
                raise web.seeother(web.ctx.homedomain)
        else:
            raise web.seeother(web.ctx.homedomain) 

    def logout(self):  
        web.ctx.session.loggedIn = False

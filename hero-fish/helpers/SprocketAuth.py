import web

class SprocketAuth(object):
    def __init__(self, app):
        self.session = web.session.Session(app, web.session.DiskStore('sessions'))

        def session_hook():
            web.ctx.session = self.session

        app.add_processor(web.loadhook(session_hook))

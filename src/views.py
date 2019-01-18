from datetime import datetime
import os
import webapp2
import jinja2

from google.appengine.ext import db
from webapp2_extras import sessions

from models import Serie, Sketch

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)  # dispatch the main handler
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def render_template(
            self,
            filename,
            template_values,
            **template_args
    ):
        template_values['logged'] = self.session.get('logged')
        template_values['user_email'] = self.session.get('user_email')
        template_values['user_name'] = self.session.get('user_name')
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))


class Login(BaseHandler):

    def get(self):
        if self.session.get('logged'):
            return self.redirect("/")
        else:
            return self.render_template("login.html", {})

    def post(self):
        self.session['user_name'] = self.request.get('user_name')
        self.session['user_email'] = self.request.get('user_email')
        self.session['logged'] = 'true'
        return self.redirect("/")


class Logout(BaseHandler):

    def get(self):
        if self.session.get('logged'):
            del self.session['logged']
            del self.session['user_name']
            del self.session['user_email']
        return self.redirect("/")


class Queries(BaseHandler):
    def get(self):
        return self.render_template("queries.html", {'series': [], 'sketches': []})


class Error(BaseHandler):
    def get(self, *args, **kwargs):
        self.render_template("error.html", {'code': 404, 'hint': 'El recurso que buscabas no existe'})

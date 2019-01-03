from datetime import datetime
import os
import webapp2
import jinja2

from google.appengine.ext import db

from models import Serie, Adds 

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

class BaseHandler(webapp2.RequestHandler):

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))


class ShowAdds(BaseHandler):
    
    def get(self):
        adds = Adds.all()
        self.render_template('adds.html', {'adds': adds})
        
class NewAdd(BaseHandler):

    def post(self):
        add = Adds(author=self.request.get('inputAuthor'),
                  text=self.request.get('inputText'),
                  priority=int(self.request.get('inputPriority')))
        add.put()
        return webapp2.redirect('/')

    def get(self):
        self.render_template('new.html', {})


class EditSerie(BaseHandler):

    def post(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        serie.title = self.request.get('inputTitle')
        serie.score = int(self.request.get('inputScore'))        
        serie.author_name = self.request.get('inputName')
        serie.author_email = self.request.get('inputEmail')
        serie.views = int(self.request.get('inputViews'))
        serie.put()
        return webapp2.redirect('/')

    def get(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        self.render_template('editSerie.html', {'serie': serie})


class DeleteAdd(BaseHandler):

    def get(self, add_id):
        iden = int(add_id)
        add = db.get(db.Key.from_path('Adds', iden))
        db.delete(add)
        return webapp2.redirect('/')



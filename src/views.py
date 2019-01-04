from datetime import datetime
import os
import webapp2
import jinja2

from google.appengine.ext import db

from models import Adds, Serie

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


##
#    SERIES
##

# class CrearSerie(BaseHandler):
class NewSerie(BaseHandler):


    def get(self):
        return self.render_template("series/new.html", {})

    def post(self):

        error = None
        p = {
            'title': self.request.get('inputTitle'),
            'author_name': self.request.get('inputAuthorName'),
            'author_email': self.request.get('inputAuthorEmail'),
            'views': 0,
            'score': self.request.get('inputScore'),

        }

        # Input validation
        if not p['title']:
            error = 'El titulo esta vacio';
        if not p['author_name']:
            error = 'El autor esta vacio'
        if not p['author_email']:
            error = 'El correo esta vacio'
        try:
            # Cambiar el modelo de int a float
            p['score'] = long(p['score'])
        except ValueError:
            error = 'La puntuacion debe ser un numero'

        if error:
            p['error'] = error
            return self.render_template("series/new.html", p)

        try:
            serie = Serie(title=p['title'], score=p['score'], author_name=p['author_name'], author_email=p['author_email'], views=p['views'])
            serie.put()
            return webapp2.redirect('/series/list')
        except Exception as e:
            p['error'] = 'No se pudo crear por {}'.format(e.message)
            return self.render_template("series/new.html", p)


class ListSeries(BaseHandler):
    def get(self):
        series = Serie.all()
        self.render_template('/series/list.html', {'series': series})
        
#     def post(self):
#         series = Serie(title = self.request.get('title'),
#                        author_name = self.request.get('author_name'),
#                        author_email = self.request.get('author_email'),
#                        score = self.request.get('score')
#                         )
#         series.put()
#         
#         return webapp2.redirect('/series/list')
               

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


class EditAdd(BaseHandler):

    def post(self, add_id):
        iden = int(add_id)
        add = db.get(db.Key.from_path('Adds', iden))
        add.author = self.request.get('inputAuthor')
        add.text = self.request.get('inputText')
        add.priority = int(self.request.get('inputPriority'))
        add.date = datetime.now()
        add.put()
        return webapp2.redirect('/')

    def get(self, add_id):
        iden = int(add_id)
        add = db.get(db.Key.from_path('Adds', iden))
        self.render_template('edit.html', {'add': add})


class DeleteAdd(BaseHandler):

    def get(self, add_id):
        iden = int(add_id)
        add = db.get(db.Key.from_path('Adds', iden))
        db.delete(add)
        return webapp2.redirect('/')


class ShowSerie(BaseHandler):

    def get(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        self.render_template('/series/showSerie.html', {'serie': serie})
        
        

class EditSerie(BaseHandler):

    def post(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))        
               
        error = None
        serie.title = self.request.get('inputTitle')
        serie.author_name = self.request.get('inputName')
        serie.author_email = self.request.get('inputEmail')
        serie.score = int(self.request.get('inputScore'))          
        
        
        # Input validation
        if not serie.title:
            error = 'El titulo esta vacio';
        if not serie.author_name:
            error = 'El autor esta vacio'
        if not serie.author_email:
            error = 'El correo esta vacio'
        try:
            # Cambiar el modelo de int a float
            serie.score = long(serie.score)
        except ValueError:
            error = 'La puntuacion debe ser un numero'

        try:            
            serie.put()
            return webapp2.redirect('/series/list')
        except Exception as e:
            error = 'No se pudo crear por {}'.format(e.message)                   

    def get(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        self.render_template('series/edit.html', {'serie': serie})
        
        
class DeleteSerie(BaseHandler):

    def get(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        db.delete(serie)
        return webapp2.redirect('/series/list')



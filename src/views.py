from datetime import datetime
import os
import webapp2
import jinja2

from google.appengine.ext import db

from models import Serie, Sketch

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
            serie = Serie(title=p['title'], score=p['score'], author_name=p['author_name'],
                          author_email=p['author_email'], views=p['views'])
            serie.put()
            return webapp2.redirect('/series/')
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
#         return webapp2.redirect('/series/')


class ShowSerie(BaseHandler):

    def get(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))

        if not serie:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna Serie con esa ID'})

        serie.views += 1
        serie.put()
        self.render_template('series/show.html', {'serie': serie})


class EditSerie(BaseHandler):

    def get(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))

        if not serie:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna Serie con esa ID'})

        error = None
        p = {
            'title': serie.title,
            'author_name': serie.author_name,
            'author_email': serie.author_email,
            'score': serie.score,
        }

        self.render_template('series/edit.html', p)

    def post(self, serie_id):

        error = None
        p = {
            'title': self.request.get('inputTitle'),
            'author_name': self.request.get('inputName'),
            'author_email': self.request.get('inputEmail'),
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
            return self.render_template("series/edit.html", p)

        try:
            iden = int(serie_id)
            serie = db.get(db.Key.from_path('Serie', iden))
            serie.title = p['title']
            serie.author_name = p['author_name']
            serie.author_email = p['author_email']
            serie.score = p['score']
            serie.put()
            return webapp2.redirect('/')
        except Exception as e:
            p['error'] = 'No se pudo editar por {}'.format(e.message)
            return self.render_template("series/edit.html", p)


class DeleteSerie(BaseHandler):

    def get(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        db.delete(serie)
        return webapp2.redirect('/series/')


class ShowSketch(BaseHandler):
    def get(self):
        webapp2.redirect("/")


class NewSketch(BaseHandler):
    def get(self):
        webapp2.redirect("/")


class EditSketch(BaseHandler):

    def get(self, add_id):
        webapp2.redirect("/")


class DeleteSketch(BaseHandler):

    def get(self, add_id):
        webapp2.redirect("/")

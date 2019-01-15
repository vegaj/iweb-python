from datetime import datetime

from google.appengine.ext import db
from views import BaseHandler
from models import Serie


class NewSerie(BaseHandler):

    def get(self):
        if self.session.get('logged') is not None:
            return self.render_template("series/new.html", {"author_name": self.session.get("user_name"), "author_email": self.session.get("user_email"),})
        else:
            return self.redirect("/login")

    def post(self):

        if self.session.get('logged') is None:
            return self.redirect("/login")

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
            return self.redirect('/series/')
        except Exception as e:
            p['error'] = 'No se pudo crear por {}'.format(e.message)
            return self.render_template("series/new.html", p)


class ListSeries(BaseHandler):
    def get(self):
        series = Serie.all()
        self.render_template('/series/list.html', {'series': series})


class ShowSerie(BaseHandler):

    def get(self, serie_id):
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))

        if not serie:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna Serie con esa ID'})

        serie.views += 1
        serie.put()

        sketches = serie.sketches if serie.sketches else []
        self.render_template('series/show.html', {'serie': serie, 'sketches': sketches})


class EditSerie(BaseHandler):

    def get(self, serie_id):
        if self.session.get('logged') is None:
            return self.redirect("/login")

        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))

        if not serie:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna Serie con esa ID'})

        if serie.author_name != self.session.get('user_name') or serie.author_email != self.session.get('user_email'):
            return self.render_template("error.html", {'code': 403, 'hint': 'No tienes permiso para editar la serie'})

        error = None
        p = {
            'title': serie.title,
            'author_name': serie.author_name,
            'author_email': serie.author_email,
            'score': serie.score,
        }

        self.render_template('series/edit.html', p)

    def post(self, serie_id):
        if self.session.get('logged') is None:
            return self.redirect("/login")

        error = None
        p = {
            'title': self.request.get('inputTitle'),
            'author_name': self.request.get('inputName'),
            'author_email': self.request.get('inputEmail'),
            'score': self.request.get('inputScore'),

        }

        # Input validation
        if not p['title']:
            error = 'El titulo esta vacio'
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
            if serie.author_name != self.session.get('user_name') or serie.author_email != self.session.get('user_email'):
                return self.render_template("error.html", {'code': 403, 'hint': 'No tienes permiso para editar la serie'})
            serie.title = p['title']
            serie.score = p['score']
            serie.put()
            return self.redirect('/')
        except Exception as e:
            p['error'] = 'No se pudo editar por {}'.format(e.message)
            return self.render_template("series/edit.html", p)


class DeleteSerie(BaseHandler):

    def get(self, serie_id):
        if self.session.get('logged') is None:
            return self.redirect("/login")

        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        if not serie:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna Serie con esa ID'})

        if serie.author_name != self.session.get('user_name') or serie.author_email != self.session.get('user_email'):
            return self.render_template("error.html", {'code': 403, 'hint': 'No tienes permiso para borrar la serie'})

        db.delete(serie)
        return self.redirect('/series/')

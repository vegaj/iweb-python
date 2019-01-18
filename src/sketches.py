from datetime import datetime

from google.appengine.ext import db
from views import BaseHandler
from models import Sketch


class ShowSketch(BaseHandler):
    
    def get(self, sketch_id):
        iden = int(sketch_id)
        sketch = db.get(db.Key.from_path('Sketch', iden))
        if not sketch:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna vi\u00F1eta con esa ID'})

        comments = sketch.comments if sketch.comments else []
        self.render_template('sketches/show.html', {'sketch': sketch, 'comments': comments})
    

class NewSketch(BaseHandler):

    def get(self, serie_id):
        if self.session.get('logged') is None:
            return self.redirect("/login")

        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        if not serie:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna Serie con esa ID'})
        if not serie.belongs_to(self.session.get('user_email')):
            return self.render_template("error.html", {'code': 403, 'hint': 'No tienes permiso para crear un sketch en la serie'})
        return self.render_template("sketches/new.html", {})

    def post(self, serie_id):
        if self.session.get('logged') is None:
            return self.redirect("/login")
        error = None
        p = {'title': self.request.get('inputTitle'),
             'score': self.request.get('inputScore')
             }

        # Input validation
        if not p['title']:
            error = 'El titulo esta vacio';

        try:
            # Cambiar el modelo de int a float
            p['score'] = long(p['score'])
        except ValueError:
            error = 'La puntuacion debe ser un numero'

        if error:
            p['error'] = error
            return self.render_template('sketches/new.html', p)

        iden = int(serie_id)
        serie1 = db.get(db.Key.from_path('Serie', iden))
        if not serie1:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna Serie con esa ID'})
        if not serie1.belongs_to(self.session.get('user_email')):
            return self.render_template("error.html",
                                        {'code': 403, 'hint': 'No tienes permiso para crear un sketch en la serie'})
        try:
            sk = Sketch(title=p['title'],
                        createdAt=datetime.now(),
                        score=p['score'],
                        serie=serie1
                        )
            sk.put()
            return self.redirect('/series/show/{}'.format(sk.serie.key().id()))
        except Exception as e:
            p['error'] = 'No se pudo crear por {}'.format(e.message)
            return self.render_template("error.html", {'code': 500, 'hint': p['error']})


class EditSketch(BaseHandler):

    def get(self, sketch_id):
        if self.session.get('logged') is None:
            return self.redirect("/login")
        iden = int(sketch_id)
        sketch = db.get(db.Key.from_path('Sketch', iden))

        if not sketch:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna vi\u00F1eta con esa ID'})
        if not sketch.serie.belongs_to(self.session.get('user_email')):
            return self.render_template("error.html",
                                        {'code': 403, 'hint': 'No tienes permiso para editar un sketch en la serie'})

        p = {
            'title': sketch.title,
            'createdAt': sketch.createdAt,
            'score': sketch.score,
        }

        self.render_template('sketches/edit.html', p)

    def post(self, sketch_id):
        if self.session.get('logged') is None:
            return self.redirect("/login")

        error = None
        p = {
            'title': self.request.get('inputTitle'),
            'createdAt': self.request.get('inputCreatedAt'),
            'score': self.request.get('inputScore'),

        }

        # Input validation
        if not p['title']:
            error = 'El titulo esta vacio';

        try:
            date = datetime.strptime(p['createdAt'], '%Y-%m-%d')
            print(date)
            if date.year < 1900:
                p['createdAt'] = datetime.today()
                error = "La fecha debe ser mayor a 01-01-1900"
            else:
                p['createdAt'] = date
        except ValueError:
            p['createdAt'] = datetime.today()
            error = 'La fecha es incorrecta'

        try:
            # Cambiar el modelo de int a float
            p['score'] = long(p['score'])
        except ValueError:
            error = 'La puntuacion debe ser un numero'

        if error:
            p['error'] = error
            return self.render_template("sketches/edit.html", p)

        try:
            iden = int(sketch_id)
            sketch = db.get(db.Key.from_path('Sketch', iden))
            if not sketch:
                return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna vi\u00F1eta con esa ID'})
            if not sketch.serie.belongs_to(self.session.get('user_email')):
                return self.render_template("error.html", {'code': 403, 'hint': 'No tienes permiso para editar la serie'})

            sketch.title = p['title']
            sketch.createdAt = p['createdAt']
            sketch.score = p['score']
            sketch.put()
            return self.redirect('/series/show/{}'.format(sketch.serie.key().id()))
        except Exception as e:
            p['error'] = 'No se pudo editar por {}'.format(e.message)
            return self.render_template("error.html", {'code': 500, 'hint': p['error']})


class DeleteSketch(BaseHandler):

    def get(self, sketch_id):
        if self.session.get('logged') is None:
            return self.redirect("/login")
        iden = int(sketch_id)
        sketch = db.get(db.Key.from_path('Sketch', iden))
        if not sketch:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna vi\u00F1eta con esa ID'})
        if not sketch.serie.belongs_to(self.session.get('user_email')):
            return self.render_template("error.html",
                                        {'code': 403, 'hint': 'No tienes permiso para borrar un sketch en la serie'})
        id_serie = sketch.serie.key().id()
        sketch.cascade()
        return self.redirect('/series/show/{}'.format(id_serie))


class BestScoreSketches(BaseHandler):
    
    def get(self):
        sketches = db.GqlQuery("SELECT * FROM Sketch ORDER BY score DESC")
        self.render_template('queries.html', {'sketches': sketches})


class TopDateSketches(BaseHandler):
    
    def get(self):
        sketches = db.GqlQuery("SELECT * FROM Sketch ORDER BY createdAt DESC")
        self.render_template('queries.html', {'sketches': sketches})

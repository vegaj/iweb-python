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
        iden = int(serie_id)
        serie = db.get(db.Key.from_path('Serie', iden))
        if not serie:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna Serie con esa ID'})
        return self.render_template("sketches/new.html", {})

    def post(self, serie_id):
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
        iden = int(sketch_id)
        sketch = db.get(db.Key.from_path('Sketch', iden))

        if not sketch:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna vi\u00F1eta con esa ID'})

        p = {
            'title': sketch.title,
            'createdAt': sketch.createdAt,
            'score': sketch.score,
        }

        self.render_template('sketches/edit.html', p)

    def post(self, sketch_id):

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
            p['createdAt'] = datetime.strptime(p['createdAt'], '%Y-%m-%d')
        except ValueError:
            error = 'La fecha esta vacia'

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
        iden = int(sketch_id)
        sketch = db.get(db.Key.from_path('Sketch', iden))
        if not sketch:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ninguna vi\u00F1eta con esa ID'})
        id_serie = sketch.serie.key().id()
        db.delete(sketch)
        return self.redirect('/series/show/{}'.format(id_serie))

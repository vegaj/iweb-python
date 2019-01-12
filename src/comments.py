from datetime import datetime

from google.appengine.ext import db
from views import BaseHandler
from models import Comment

class NewComment(BaseHandler):

    def get(self, sketch_id):
        iden = int(sketch_id)
        sketch = db.get(db.Key.from_path('Sketch', iden))
        if not sketch:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ningun sketch con esa ID'})
        return self.render_template("comments/new.html", {})

    def post(self, sketch_id):
        error = None
        p = {'author_name': self.request.get('inputAuthor'),
             'author_email': self.request.get('inputEmail'),
             'text': self.request.get('inputText')
             }

        # Input validation
        if not p['author_name']:
            error = 'El nombre del autor esta vacio';
        
        if not p['author_email']:
            error = 'El email del autor esta vacio';
            
        if not p['text']:
            error = 'El texto esta vacio';

        if error:
            p['error'] = error
            return self.render_template('comments/new.html', p)

        iden = int(sketch_id)
        sketch1 = db.get(db.Key.from_path('Sketch', iden))
        if not sketch1:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ningun sketch con esa ID'})

        try:
            comment = Comment(author_name=p['author_name'],
                        author_email=p['author_email'],
                        lastEdit=datetime.now(),
                        text=p['text'],
                        sketch=sketch1
                        )
            comment.put()
            return self.redirect('/series/')
        except Exception as e:
            p['error'] = 'No se pudo crear por {}'.format(e.message)
            return self.render_template("error.html", {'code': 500, 'hint': p['error']})
        
class DeleteComment(BaseHandler):

    def get(self, comment_id):
        iden = int(comment_id)
        comment = db.get(db.Key.from_path('Comment', iden))
        if not comment:
            return self.render_template("error.html", {'code': 404, 'hint': 'No existe ningun comentario con esa ID'})
        db.delete(comment)
        return self.redirect('/series/')
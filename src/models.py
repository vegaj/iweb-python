from google.appengine.ext import db
import util


class Serie(db.Model):
    title = db.StringProperty()
    score = db.IntegerProperty()
    author_name = db.StringProperty()
    author_email = db.EmailProperty()
    views = db.IntegerProperty()

    def belongs_to(self, user_email):
        return util.is_authorized(user_email, self.author_email)

    def cascade(self):
        for s in self.sketches:
            s.cascade()
        db.delete(self)


class Sketch(db.Model):
    title = db.StringProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    score = db.IntegerProperty()
    photo_url = db.StringProperty()
    serie = db.ReferenceProperty(Serie, collection_name='sketches')

    def belongs_to(self, user_email):
        return util.is_authorized(user_email, self.serie.author_email)

    def cascade(self):
        for c in self.comments:
            c.cascade()
        db.delete(self)


class Comment(db.Model):
    author_name = db.StringProperty()
    author_email = db.EmailProperty()
    text = db.StringProperty(required=True, multiline=True)
    lastEdit = db.DateTimeProperty(auto_now=True)
    sketch = db.ReferenceProperty(Sketch, collection_name='comments', required=True)

    def belongs_to(self, user_email):
        return util.is_authorized(user_email, self.author_email)

    def cascade(self):
        db.delete(self)

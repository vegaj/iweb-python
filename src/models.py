from google.appengine.ext import db


class Adds(db.Model):

    author = db.EmailProperty()
    text = db.StringProperty()
    priority = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)


class Serie(db.Model):

    title = db.StringProperty()
    score = db.IntegerProperty()
    author_name = db.StringProperty()
    author_email = db.EmailProperty()
    views = db.IntegerProperty()


class Sketch(db.Model):
    title = db.StringProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    score = db.IntegerProperty()
    serie = db.ReferenceProperty(Serie, collection_name='sketches')


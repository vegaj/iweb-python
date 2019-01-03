from google.appengine.ext import db


class Adds(db.Model):

    author = db.EmailProperty()
    text = db.StringProperty()
    priority = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    

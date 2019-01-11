from views import Login, Logout, Error
from series import NewSerie, ListSeries, ShowSerie, EditSerie, DeleteSerie
from sketches import NewSketch, EditSketch, DeleteSketch 
from comments import NewComment, DeleteComment
import webapp2
from cgitb import handler

config = {'webapp2_extras.sessions': {
    'secret_key': 'my-super-secret-key',
}}

app = webapp2.WSGIApplication([
        ('/', ListSeries),
        ('/login', Login),
        ('/logout', Logout),
        ('/sketches/edit/([\d]+)', EditSketch),
        ('/sketches/delete/([\d]+)', DeleteSketch),
        ('/series/', ListSeries),
        ('/series/new', NewSerie),
        ('/series/show/([\d]+)', ShowSerie),
        ('/series/edit/([\d]+)', EditSerie),
        ('/series/delete/([\d]+)', DeleteSerie),
        ('/series/([\d]+)/sketches/new', NewSketch),
        ('/sketches/([\d]+)/comments/new', NewComment),
        ('/comments/delete/([\d]+)', DeleteComment),
        (r'/<:.*>', Error),
        ],
        config=config,
        debug=True)

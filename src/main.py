from views import Login, Logout
from series import NewSerie, ListSeries, ShowSerie, EditSerie, DeleteSerie
from sketches import NewSketch, EditSketch, DeleteSketch 
import webapp2

config = {'webapp2_extras.sessions': {
    'secret_key': 'my-super-secret-key',
}}

app = webapp2.WSGIApplication([
        ('/', ListSeries),
        ('/login', Login),
        ('/logout', Logout),
        ('/sketches/new', NewSketch),
        ('/sketches/edit/([\d]+)', EditSketch),
        ('/sketches/delete/([\d]+)', DeleteSketch),
        ('/series/', ListSeries),
        ('/series/new', NewSerie),
        ('/series/show/([\d]+)', ShowSerie),
        ('/series/edit/([\d]+)', EditSerie),
        ('/series/delete/([\d]+)', DeleteSerie),
        ('/series/([\d]+)/sketches/new', NewSketch),
        ],
        config=config,
        debug=True)

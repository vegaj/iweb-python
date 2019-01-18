from views import Login, Logout, Error, Queries
from series import NewSerie, ListSeries, ShowSerie, EditSerie, DeleteSerie, MostViewedSeries, BestScoreSeries, SearchSeries
from sketches import NewSketch, EditSketch, DeleteSketch, ShowSketch, BestScoreSketches, TopDateSketches
from comments import NewComment, DeleteComment, EditComment
import webapp2
from webapp2 import Route
from cgitb import handler
from comicvines import ComicVine
config = {'webapp2_extras.sessions': {
    'secret_key': 'my-super-secret-key',
}}

app = webapp2.WSGIApplication([
        ('/', ListSeries),
        ('/login', Login),
        ('/logout', Logout),
        ('/sketches/show/([\d]+)', ShowSketch),
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
        ('/comments/edit/([\d]+)', EditComment),
        ('/comicvine/', ComicVine),
        ('/series/mostViewed/', MostViewedSeries),
        ('/series/bestScore/', BestScoreSeries),
        ('/sketches/bestScore/', BestScoreSketches),
        ('/sketches/topDate/', TopDateSketches),
        ('/series/search/', SearchSeries),
        ('/queries/', Queries), 
        Route(r'/<:.*>', handler=Error),
        ],
        config=config,
        debug=True)

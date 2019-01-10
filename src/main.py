from views import NewSerie, ListSeries, ShowSerie, EditSerie, DeleteSerie, NewSketch, EditSketch, DeleteSketch
import webapp2

app = webapp2.WSGIApplication([
        ('/', ListSeries),
        ('/sketches/edit/([\d]+)', EditSketch),
        ('/sketches/delete/([\d]+)', DeleteSketch),
        ('/series/', ListSeries),
        ('/series/new', NewSerie),
        ('/series/show/([\d]+)', ShowSerie),
        ('/series/edit/([\d]+)', EditSerie),
        ('/series/delete/([\d]+)', DeleteSerie),
        ('/series/([\d]+)/sketches/new', NewSketch),
        ],
        debug=True)

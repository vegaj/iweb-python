from views import ShowAdds, NewAdd, DeleteAdd, EditAdd, NewSerie, ListSeries
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowAdds), 
        ('/new', NewAdd), 
        ('/edit/([\d]+)', EditAdd),
        ('/delete/([\d]+)', DeleteAdd),
        ('/series/list', ListSeries),
        ('/series/new', NewSerie)
        ],
        debug=True)

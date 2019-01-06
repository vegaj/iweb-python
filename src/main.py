from views import ShowAdds, NewAdd, DeleteAdd, EditAdd, NewSerie, ListSeries, ShowSerie, EditSerie, DeleteSerie
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowAdds), 
        ('/new', NewAdd), 
        ('/edit/([\d]+)', EditAdd),
        ('/delete/([\d]+)', DeleteAdd),
        ('/series/list', ListSeries),
        ('/series/new', NewSerie),
        ('/series/showSerie/([\d]+)', ShowSerie),
        ('/series/edit/([\d]+)', EditSerie),
        ('/series/delete/([\d]+)', DeleteSerie),
        ],
        debug=True)
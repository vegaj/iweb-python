from views import ShowAdds, NewAdd, DeleteAdd, EditAdd, ShowSerie
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowAdds), 
        ('/new', NewAdd), 
        ('/edit/([\d]+)', EditAdd),
        ('/delete/([\d]+)', DeleteAdd),        
        ('/showSerie/([\d]+)', ShowSerie),
        ],
        debug=True)

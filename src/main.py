from views import ShowAdds, NewAdd, DeleteAdd, EditAdd, DeleteSerie
import webapp2

app = webapp2.WSGIApplication([
         ('/', ShowAdds), 
        ('/new', NewAdd), 
        ('/edit/([\d]+)', EditAdd),
        ('/delete/([\d]+)', DeleteAdd),
        ('/series/delete/([\d]+)', DeleteSerie),
        ],
        debug=True)

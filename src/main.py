from views import ShowAdds, NewAdd, DeleteAdd, EditAdd, EditSerie
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowAdds), 
        ('/new', NewAdd), 
        ('/edit/([\d]+)', EditAdd),
        ('/delete/([\d]+)', DeleteAdd),
        ('/series/edit/([\d]+)', EditSerie),
        ],
        debug=True)
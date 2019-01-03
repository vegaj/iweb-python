from views import ShowAdds, NewAdd, DeleteAdd, EditAdd, CrearSerie
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowAdds), 
        ('/new', NewAdd), 
        ('/edit/([\d]+)', EditAdd),
        ('/delete/([\d]+)', DeleteAdd),
        ('/series/new', CrearSerie)
        ],
        debug=True)

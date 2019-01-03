from views import ShowAdds, NewAdd, DeleteSerie, EditAdd
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowAdds), 
        ('/new', NewAdd), 
        ('/edit/([\d]+)', EditAdd),
        ('/delete/([\d]+)', DeleteSerie),
        ],
        debug=True)

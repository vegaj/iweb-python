from views import ShowAdds, NewAdd, DeleteAdd, EditSerie
import webapp2

app = webapp2.WSGIApplication([
        ('/', ShowAdds), 
        ('/new', NewAdd), 
        ('/editSerie/([\d]+)', EditSerie),
        ('/delete/([\d]+)', DeleteAdd),
        ],
        debug=True)
# coding: utf-8
from views import BaseHandler
from os import environ
from google.appengine.api import urlfetch
import json

class ComicVine(BaseHandler):
    API_KEY = environ.get('COMIC_KEY')
    BASE_PATH = "https://comicvine.gamespot.com/api"

    def get(self):
        """Devolvemos el template y su contexto"""
        ctx = {}

        return self.render_template("comicvine.html", ctx)

    def post(self):
        """Devolvemos el template, su contexto y los resultados de la petición"""
        ctx = {
            'title': 'spid'
        }

        try:
            query = self.generate_query(ctx)
            result = urlfetch.fetch(query)
            result = json.loads(result.content)
            status = int(result.get('status_code'))
            results = []
            error = None

            if status is 1:
                results = result.get('results')
            elif status is 104:
                error = u"El filtro no es válido"
            elif status is 101:
                error = u"No se ha encontrado nada"
            else:
                return self.render_template("error.html", {'error': u'El servicio no está disponible'})

            return self.render_template("comicvine.html", {'error': error, 'results': results, 'query': query})
        except ValueError as e:
            ctx['error'] = u'{Se esperaba un entero positivo en el campo {}'.format(e.message)
        except NameError as e:
            ctx['error'] = u'{}'.format(e.message)
        except Exception as e:
            ctx['error'] = u'{}'.format(e)
        return self.render_template("comicvine.html", ctx)

    def generate_query(self, opt):
        opt['base'] = self.BASE_PATH
        opt['key'] = self.API_KEY

        title = opt.get('title')
        if title is None:
            raise NameError(u'Se necesita un término de búsqueda')

        opt['limit'] = self.extract_positive_integer(opt, 'limit', val_def=10)
        opt['offset'] = self.extract_positive_integer(opt, 'offset', val_def=0)
        fields = opt.get('fields')
        fields = fields if fields is not None else ['count_of_episodes', 'name', 'site_detail_url',
                                                                  'publisher', 'image']
        opt['fields_str'] = ','.join(fields)

        uri = "{base}/series_list?format=json&limit={limit}&offset={offset}&api_key={key}&filter=name:{" \
              "title}&field_list={fields_str}".format(**opt)
        return uri

    def extract_positive_integer(self, dict, key, val_def=0):
        """Este método devolvera val_def en caso de que no esté presente o sea inválido"""
        v = dict.get(key)

        if v is None:
            v = val_def
        try:
            v = int(v)
        except ValueError:
            v = val_def
        return v

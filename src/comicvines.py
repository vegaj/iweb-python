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
        ctx = {'api_key': self.API_KEY}

        return self.render_template("comicvine.html", ctx)

    def post(self):
        """Devolvemos el template, su contexto y los resultados de la petición"""
        ctx = {
            'title': self.request.get("search-term")
        }

        query = self.generate_query(ctx)
        ctx['query'] = query
        result = urlfetch.fetch(query)
        result = json.loads(result.content)
        status = int(result.get('status_code'))

        if status is 1:
            results = []
            for e in result.get('results'):
                results.append(e)
            ctx['results'] = results
        elif status is 104:
            ctx['error'] = u"El filtro no es válido"
        elif status is 101:
            ctx['error'] = u"No se ha encontrado nada"
        elif status is 100:
            ctx['error'] = u"Se ha excecido el límite de consultas sobre la api."
            ctx['code'] = 403
            return self.render_template("error.html", ctx);
        else:
            ctx['error'] = u'El servicio no está disponible'
            ctx['code'] = 500
            return self.render_template("error.html", ctx)

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


    @staticmethod
    def extract_positive_integer(dict, key, val_def=0):
        """Este método devolvera val_def en caso de que no esté presente o sea inválido"""
        v = dict.get(key)

        if v is None:
            v = val_def
        try:
            v = int(v)
        except ValueError:
            v = val_def
        return v

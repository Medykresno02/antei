from requests import get
from bs4 import BeautifulSoup as bs
from json import loads
from utilities import jsonify

class wpObj:

    def __init__(self, data) -> None:
        self.res = loads(data.strip().strip('window.prefetched =').strip(';'))['search.stories.results.anime.false.false']['data']

    @property
    def fetch(self):
        return [{'id': _.get('id'), 'title': _.get('title'), 'user': _.get('user'), 'votes': _.get('voteCount'), 'reads': _.get('readCount'), 'comments': _.get('commentCount'), 'mature': bool(_.get('mature')), 'url': _.get('url'), 'thumbnail': _.get('cover').replace('256','725'), 'completed': bool(_.get('completed'))} for _ in self.res.get('stories')]

class search:

    def __init__(self, query) -> None:
        self.hasil = wpObj(bs(get('https://www.wattpad.com/search/%s' % query, headers={'User-Agent': 'Googlebot'}).text, 'html.parser').findAll('script', type='text/javascript')[12].string).fetch

    def __str__(self) -> str:
        return '<[count %s]>' % self.hasil.__len__()

    def __repr__(self) -> str:
        return self.__str__()

def wattpad(req):
    if (query := req.GET.get('query')):
        return jsonify({'status': 200, 'result': search(query).hasil}, 200)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter query jangan kosong'}, 400)

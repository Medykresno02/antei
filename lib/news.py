from bs4 import BeautifulSoup as bs
from requests import get
from html2text import html2text
from utilities import jsonify

def cnbc(req):
    """
    kategori: news, terbaru, investment, market, entreprenur, syariah, tech, lifestyle, opini, profil
    """
    if (kategori := req.GET.get('kategori')):
        kate = {'news':'https://www.cnbcindonesia.com/news/rss','terbaru': 'https://www.cnbcindonesia.com/rss','investment': 'https://www.cnbcindonesia.com/investment/rss','market': 'https://www.cnbcindonesia.com/market/rss','entreprenur': 'https://www.cnbcindonesia.com/entreprenur/rss','syariah': 'https://www.cnbcindonesia.com/syariah/rss','tech': 'https://www.cnbcindonesia.com/tech/rss','lifestyle': 'https://www.cnbcindonesia.com/lifestyle/rss','opini': 'https://www.cnbcindonesia.com/opini/rss','profil': 'https://www.cnbcindonesia.com/profil/rss'}
        if not kate.get(kategori.lower()):return jsonify({'status': 400, 'msg': f'kategori yang tersedia hanya : {kate.keys().__str__().strip("dict_keys(").strip(")")}'}, 400)
        ikeh = bs(get(kate.get(kategori.lower())).text, 'xml')
        title = [html2text(ahh.text).strip() for ahh in ikeh.findAll('title')[2::]]
        desc = [kimochii.text for kimochii in ikeh.findAll('content:encoded')]
        thumb = [omangko['url'].replace('360','1280').replace('90','720') for omangko in ikeh.findAll('enclosure')]
        url = [ochinpo.text for ochinpo in ikeh.findAll('link')[3::]]
        pub = [oshiri.text for oshiri in ikeh.findAll('pubDate')]
        results = [{"title": title[oppai], "description": desc[oppai], "url": url[oppai], "thumbnail": thumb[oppai], "pubdate": pub[oppai]} for oppai, _ in enumerate(title)]
        return jsonify({'status': 200, 'result': results}, 200)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter kategori jangan kosong'}, 400)

def antara():
    try:
        ikeh = bs(get("https://www.antaranews.com/rss/top-news.xml").text, "xml")
        kimochii = [{"title": i.title.text, "description": html2text(i.find("content:encoded").text).strip(), "url": i.link.text, "thumbnail": i.enclosure.get("url"), "pubdate": i.pubDate.text} for i in ikeh.findAll("item")]
        return jsonify({"status": 200, "result": kimochii}, 200)
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan"}, 409)

def suara():
    try:
        ikeh = bs(get("https://www.suara.com/rss/news").text, "xml")
        kimochii = [{"title": i.title.text.strip(), "description": html2text(i.description.text.split("/>")[1].strip()).strip(), "url": i.link.text, "thumbnail": i.enclosure.get("url"), "pubdate": i.pubDate.text} for i in ikeh.findAll("item")]
        return jsonify({"status": 200, "result": kimochii})
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan"}, 409)

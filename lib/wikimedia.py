from utilities import jsonify
from requests import get

def wikme(req):
    if (quer := req.GET.get('query')):
        try:
            result = get("https://commons.wikimedia.org/w/api.php?action={}&generator={}&prop=imageinfo&gimlimit={}&redirects=1&titles={}&iiprop={}&format={}".format("query","images","10",quer,"timestamp|user|url|mime|thumbmime|mediatype","json")).json()['query']['pages']
            results = []
            for _ in result:
                results.append({
                'pageid': cv['pageid'],
                'title': cv['title'],
                'imageinfo': cv['imageinfo'][0],
                'timestamp': cv['timestamp'],
                'user': cv['user'],
                'descriptionUrl': cv['descriptionurl'],
                'mime': cv['mime'],
                'mediatype': cv['mediatype']
                })
            return jsonify({'status': 200, 'result': results}, 200)
        except Exception as e:
            print(e)
            return jsonify({'status': 409, 'msg': 'Terjadi kesalahan, yang anda cari tidak ada'}, 409)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter query jangan kosong'}, 400)

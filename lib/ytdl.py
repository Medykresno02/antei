from requests import get
from youtubesearchpython import Video, SearchVideos
from utilities import h2k, jsonify
from humanfriendly import format_timespan as fts
from re import match
import pafy
pafy.set_api_key('AIzaSyAy9Bg7F5qiBtFepwN4CWRfOiftux4z5yU')

def get_id(url):
    pattern = r"(?:http(?:s|):\/\/|)(?:(?:www\.|)youtube(?:\-nocookie|)\.com\/(?:shorts\/)?(?:watch\?.*(?:|\&)v=|embed\/|v\/)|youtu\.be\/)([-_0-9A-Za-z]{11})"
    return match(pattern, url).group(1) if match(pattern, url) else False

def convert_size(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def get_size(url):
    return convert_size(int(get(url, stream=True, headers={'user-agent': 'Googlebot'}).headers.get('content-length')))

class YouTube:

    @staticmethod
    def yta(req):
        '''
        url : https://www.youtube.com/watch?v=6l5V3BWDcMw
        '''
        if (url := req.GET.get("url")):
            try:
                _a = pafy.new(url)
                _b = _a.getbestaudio(preftype='m4a')
                #anu = Video.get(url)
                return jsonify({
                    'status': 200,
                    #'keywords': anu['keywords'],
                    #'description': anu['description'],
                    'title': _a.title,
                    'thumb': _a.bigthumbhd,
                    'duration': fts(_a.length),
                    'bitrate': _b.bitrate,
                    'likes': h2k(_a.likes),
                    'dislikes': h2k(_a.dislikes),
                    'views': h2k(_a.viewcount),
                    'result': _b.url,
                    'filesize': convert_size(_b.get_filesize())
                }, 200)
            except Exception as e:
                print(e)
                return jsonify({
                    'status': 409,
                    'msg': 'Terjadi kesalahan, mungkin url tidak valid'
                }, 409)
        else:
            return jsonify({
                'status': 400,
                'msg': 'Parameter url jangan kosong'
            }, 400)

    @staticmethod
    def ytv(req):
        if (url := req.GET.get("url")):
            try:
                _a = pafy.new(url)
                _b = _a.getbestvideo(preftype='mp4')
                #anu = Video.get(url)
                return jsonify({
                    'status': 200,
                    #'keywords': anu['keywords'],
                    #'description': anu['description'],
                    'title': _a.title,
                    'thumb': _a.bigthumbhd,
                    'duration': fts(_a.length),
                    'quality': _b.quality,
                    'likes': h2k(_a.likes),
                    'dislikes': h2k(_a.dislikes),
                    'views': h2k(_a.viewcount),
                    'result': _b.url,
                    'filesize': convert_size(_b.get_filesize())
                }, 200)
            except Exception as e:
                print(e)
                return jsonify({
                    'status': 409,
                    'msg': 'Terjadi kesalahan, mungkin url tidak valid'
                }, 409)
        else:
            return jsonify({
                'status': 400,
                'msg': 'Parameter url jangan kosong'
            }, 400)

    @staticmethod
    def yts(req):
        if (query := req.GET.get("q")):
            try:
                _a = SearchVideos(query, mode='dict').result()['search_result']
                return jsonify({
                    'status': 200,
                    'result': _a
                }, 200)
            except Exception as e:
                print(e)
                return jsonify({
                    'status': 409,
                    'msg': 'Terjadi kesalahan, %s tidak ditemukan' % query
                }, 409)
        else:
            return jsonify({
                'status': 400,
                'msg': 'Parameter q jangan kosong'
            }, 400)

yta = YouTube.yta
ytv = YouTube.ytv
yts = YouTube.yts

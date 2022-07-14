from requests import Session, get as _get
from bs4 import BeautifulSoup as bs
from utilities import jsonify, h2k, get_file_json, gen_ipv4
from utilities.file_ import makefile
from re import search
from json import loads

class TikVid:
    def __init__(self):
        self.description:str = ""
        self.likes:int = 0
        self.comments:int = 0
        self.shares:int = 0
        self.plays:int = 0
        self.author:str = ""
        self.video:dict = {}
        self.music:dict = {}
        self.author:dict = {}

    def to_json(self, req):
        self.author["avatar"] = get_file_json(self.author["avatar"], req).get("url")
        self.video["thumbnail"] = get_file_json(self.video["thumbnail"], req).get("url")
        self.video["url_wm"] = get_file_json(self.video["url_wm"], req).get("url")
        self.video["url_nowm"] = None if self.video["url_nowm"] == None else get_file_json(self.video["url_nowm"], req).get("url")
        self.music["thumbnail"] = get_file_json(self.music["thumbnail"], req).get("url")
        self.music["url"] = get_file_json(self.music["url"], req).get("url")
        self.__dict__.update({"status": 200})
        return self.__dict__

    def __repr__(self):
        return "<username: %s>" % self.author["username"]

class TikPro:
    def __init__(self):
        self.name:str = ""
        self.username:str = ""
        self.id:int = 0
        self.avatar:str = ""
        self.description:str = ""
        self.verified:bool = False
        self.likes:int = 0
        self.followers:int = 0
        self.following:int = 0
        self.videos:int = 0

    def to_json(self, req):
        self.avatar = get_file_json(self.avatar, req).get("url")
        self.__dict__.update({"status": 200})
        return self.__dict__

    def __repr__(self):
        return "<username: %s>" % self.username

class TikTok(Session):

    def __init__(self):
        super().__init__()
        self.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
        self.tot = r'<script[^>]+\bid=["\']__NEXT_DATA__[^>]+>\s*({.+?})\s*</script'

    def deel(self, url:str=""):
        try:
            self.headers["X-Forwarded-For"] = gen_ipv4()
            res = TikVid()
            anu = self.get(url)
            ue = loads(search(self.tot, anu.text)[0].split(">")[1].strip("</script"))["props"]["pageProps"]
            cih = ue.get("itemInfo").get("itemStruct")
            if not cih and ue.get("statusCode") == 10216:
                return "Private"
            res.author["name"] = cih.get("author").get("nickname")
            res.author["id"] = cih.get("author").get("id")
            res.author["username"] = cih.get("author").get("uniqueId")
            res.author["avatar"] = makefile("avatar", self.get(cih.get("author").get("avatarLarger")).content, 60*15)
            res.author["verified"] = cih.get("author").get("verified")
            res.description = cih.get("desc")
            res.likes = cih.get("stats").get("diggCount")
            res.comments = cih.get("stats").get("commentCount")
            res.shares = cih.get("stats").get("shareCount")
            res.plays = cih.get("stats").get("playCount")
            res.video["thumbnail"] = makefile("thmb_video", self.get(cih.get("video").get("cover")).content, 60*15)
            res.video["duration"] = cih.get("video").get("duration")
            res.video["url_wm"] = makefile("vid_wm", self.get(cih.get("video").get("downloadAddr")).content, 60*15)
            res.video["url_nowm"] = self.ttdl(url)
            res.music["thumbnail"] = makefile("thmb_music", self.get(cih.get("music").get("coverLarge")).content, 60*15)
            res.music["title"] = cih.get("music").get("title")
            res.music["author"] = cih.get("music").get("authorName")
            res.music["url"] = makefile("aud", self.get(cih.get("music").get("playUrl")).content, 60*15)
            return res
        except Exception as e:
            print("deel: %s" % e)
            return False

    def ttdl(self, url):
        try:
            r = Session()
            _f = bs(r.get(f"https://ttdownloader.com/?url={url}").text, "html.parser")
            _d = {"token": _f.find("input", {"id": "token"}).get("value"), "format": None, "url": url}
            _l = bs(r.post("https://ttdownloader.com/req/", data=_d).text, "html.parser").findAll("a", {"class": "download-link"})[:3]
            return makefile("tktod_nowm", r.get(_l[0].get("href")).content, 60*15)
        except Exception as e:
            print("ttdl: %s" % e)
            return None

    def stalk(self, username:str=""):
        try:
            self.headers["X-Forwarded-For"] = gen_ipv4()
            res = TikPro()
            anu = self.get("https://www.tiktok.com/@%s" % username)
            ue = loads(search(self.tot, anu.text)[0].split(">")[1].strip('</script'))["props"]["pageProps"]
            cih = ue.get("userInfo")
            if not cih and ue.get("statusCode") != 0:
                return "Private"
            user = cih.get("user")
            stats = cih.get("stats")
            res.name = user.get("nickname")
            res.username = user.get("uniqueId")
            res.id = user.get("id")
            res.avatar = makefile("avatar", self.get(user.get("avatarLarger")).content, 60*15)
            res.description = user.get("signature")
            res.verified = user.get("verified")
            res.likes = stats.get("heartCount")
            res.followers = stats.get("followerCount")
            res.following = stats.get("followingCount")
            res.videos = stats.get("videoCount")
            return res
        except Exception as e:
            print("stalk: %s" % e)

def tiktod(req):
    if not req.GET.get("url"): return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)
    try:
        _r = TikTok()
        if (t := _r.deel(req.GET.get("url"))):
            return jsonify(t.to_json(req), 200) if t != "Private" else jsonify({"status": 409, "msg": "Terjadi kesalahan, video private"}, 409)
        else:
            return jsonify({"status": 409, "msg": "Terjadi kesalahan, mungkin url tidak valid. jika kesalahan terus belanjut lapor ke admin"}, 409)
    except Exception as e:    
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan, mungkin url tidak valid. jika kesalahan terus belanjut lapor ke admin"}, 409)

def tstalk(req):
    if not req.GET.get("username"): return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)
    try:
        _r = TikTok()
        username = req.GET.get("username").lstrip("@") if "@" in req.GET.get("username") else req.GET.get("username")
        if (t := _r.stalk(username)):
            return jsonify(t.to_json(req), 200) if t != "Private" else jsonify({"status": 409, "msg": "Terjadi kesalahan, user private"}, 409)
        else:
            return jsonify({"status": 409, "msg": "Terjadi kesalahan, mungkin username tidak valid"}, 409)
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan, mungkin username tidak valid"}, 409)
"""
def tiktod(req):
    if not req.GET.get('url'): return jsonify({'status': 400, 'msg': 'Parameter url jangan kosong'}, 400)
    try:
        _r = Session()
        _url = req.GET.get('url')
        _info = yt.extract_info(_url, False)
        _first = bs(_r.get(f'https://ttdownloader.com/?url={_url}').text, 'html.parser')
        _data = {'token': _first.find('input', id='token')['value'], 'format': None, 'url': _url}
        _last = bs(_r.post('https://ttdownloader.com/req/', data=_data).text, 'html.parser').findAll('a', class_='download-link')[:3]
        _update = _info['upload_date']
        _files = []
        for _ in [_last[0]['href'], _last[2]['href'], _info['thumbnail']]:
            _files.append(makefile(_info['id'], _r.get(_).content, 60*15))
        return jsonify({
            'status': 200,
            'description': _info['description'],
            'likes': h2k(_info['like_count']),
            'comments': h2k(_info['comment_count']),
            'reposts': h2k(_info['repost_count']),
            'duration': round(_info['duration']),
            'uploader': _info['uploader'],
            'upload_date': '%s - %s - %s' % (_update[-4:][-2:], _update[-4:][:2], _update[:4]),
            'video': get_file_json(_files[0], req),
            'audio': get_file_json(_files[1], req),
            'thumbnail': get_file_json(_files[2], req)
        }, 200)
    except Exception as e:
        print(e)
        return jsonify({
            'status': 409,
            'msg': 'Terjadi kesalahan, mungkin url tidak valid'
        }, 409)
"""

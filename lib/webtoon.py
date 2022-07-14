from requests import get, Session
from bs4 import BeautifulSoup as bs
from utilities import jsonify, get_file_json
from utilities.file_ import makefile
from PIL import Image
from io import BytesIO
from re import search

def webtuun(req):
    if (url := req.GET.get("url")):
        w = Webtoon(url).webtun
        if w:
            if isinstance(w, WebtoonInfo):
                return jsonify(w.to_json(), 200)
            elif isinstance(w, WebtoonMedia):
                w.result = get_file_json(w.result, req)
                return jsonify(w.to_json(),  200)
            else:
                return jsonify({"status": 409, "msg": "Terjadi kesalahan, mungkin url tidak valid"}, 409)
        else:
            return jsonify({"status": 409, "msg": "Terjadi kesalahan, mungkin url tidak valid"}, 409)
    else:
        return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)

class WebtoonInfo:
    def __init__(self):
        self.title = None
        self.genre = None
        self.creator = None
        self.thumbnail = None
        self.synopsis = None
        self.score = None
        self.subscribe = None
        self.episodes = []

    def to_json(self):
        self.__dict__.update({"status": 200})
        return self.__dict__

    def __repr__(self):
        return "<title: %s>" % self.title

class WebtoonMedia:
    def __init__(self):
        self.title = None
        self.episode = None
        self.result = None

    def to_json(self):
        self.__dict__.update({"status": 200})
        return self.__dict__

    def __repr__(self):
        return "<filename: %s>" % self.result.filename
        

class Webtoon:

    def __init__(self, url:str) -> None:
        """
        url: https://m.webtoons.com/id/romance/one-bite-per-month/prolog/viewer?title_no=3231&episode_no=1
        or https://m.webtoons.com/id/romance/one-bite-per-month/list?title_no=3231
        """
        self.url = url
        self.winfo = WebtoonInfo()
        self.wmedia = WebtoonMedia()

    @property
    def webtun(self):
        try:
            if "list" in self.url:
                tun = bs(get(self.url).text, "html.parser")
                self.winfo.title = tun.find("div", {"class": "info"}).h1.text
                self.winfo.genre = tun.find("div", {"class": "info"}).h2.text
                self.winfo.creator = tun.find("div", {"class": "info"}).a.text.strip().split("Info")[0].strip()
                self.winfo.thumbnail = search("(https?://[^\s]+)", tun.find("div", {"class": "detail_bg"}).get("style")).group(1)[:-1]
                self.winfo.synopsis = tun.find("p", {"class": "summary"}).text
                self.winfo.score = tun.find("em", {"class": "cnt"}).text.replace("RB","K")
                self.winfo.subscribe = tun.find("em", {"id": "_starScoreAverage"}).text
                self.winfo.episodes = [{"url": i.a.get("href"), "thumbnail": i.img.get("src"), "name": i.find("span", {"class": "subj"}).text, "date": i.find("span", {"class": "date"}).text, "likes": i.find("span", {"class": "like_area _likeitArea"}).text.split("e")[1]} for i in tun.findAll("li") if i.get("id") is not None and "episode" in i.get("id")]
                return self.winfo
            elif "viewer" in self.url:
                ses = Session()
                byte = BytesIO()
                tun = bs(ses.get(self.url).text, "html.parser")
                self.wmedia.title = tun.find("meta", {"property": "og:title"}).get("content").split("-")[0]
                self.wmedia.episode = tun.find("meta", {"property": "og:title"}).get("content").split("-")[1]
                komik = [Image.open(BytesIO(ses.get(i.get("data-url"), headers={"referer": self.url}).content)).convert("RGB") for i in tun.find("div", {"id": "_imageList"}).findAll('img')]
                komik[0].save(byte, format="PDF", save_all=True, append_images=komik)
                self.wmedia.result = makefile(f"{self.wmedia.title} - {self.wmedia.episode}", byte.getvalue(), 60*15)
                return self.wmedia
            else:
                return False
        except Exception as e:
            print(e)
            return False

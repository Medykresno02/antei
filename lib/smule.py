from requests import get
from bs4 import BeautifulSoup as bs
from re import search
from urllib.parse import quote
from utilities import jsonify

def smule_dl(req):
    if (url := req.GET.get("url")):
        smule = SmuleDL(url).deel
        if isinstance(smule, str):return jsonify({"status": 409, "msg": "Terjadi kesalahan mungkin url tidak valid"}, 409)
        smule.__dict__.update({"status": 200})
        return jsonify(smule.__dict__, 200)
    else:
        return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)

class SmuleMedia:
    def __init__(self) -> None:
        self.title = None
        self.artist = None
        self.caption = None
        self.type = None
        self.audio = None
        self.video = None
        self.loves = None
        self.gifts = None
        self.comments = None
        self.plays = None

class SmuleDL:

    def __init__(self, url) -> None:
        """
        url: https://www.smule.com/p/1998769355_3429377039
        """
        self.url = url
        self.media = SmuleMedia()

    @property
    def deel(self) -> SmuleMedia:
        try:
            smule = get(self.url).text
            soup = bs(smule, "html.parser")
            media_url = soup.find("meta", {"name": "twitter:player:stream"})["content"]
            media_type = soup.find("meta", {"name": "twitter:player:stream:content_type"})["content"]
            if media_type == "video/mp4":
                media_re = search("\"media_url\":\"(.*?)\"", smule).group(1)
                audio_url = f"{media_url.split('=e')[0]}={quote(media_re)}"
            self.media.title = search("\"title\":\"(.*?)\"", smule).group(1)
            self.media.artist = search("\"artist\":\"(.*?)\"", smule).group(1)
            self.media.caption = search("\"message\":\"(.*?)\"", smule).group(1)
            self.media.type = media_type.split("/")[0]
            self.media.audio = get(audio_url, stream=True).url if media_type == "video/mp4" else get(media_url, stream=True).url
            self.media.video = get(media_url, stream=True).url if media_type == "video/mp4" else None
            self.media.loves = search("\"truncated_loves\":\"(.*?)\"", smule).group(1)
            self.media.gifts = search("\"truncated_gifts\":\"(.*?)\"", smule).group(1)
            self.media.comments = search("\"truncated_comments\":\"(.*?)\"", smule).group(1)
            self.media.plays = search("\"truncated_listens\":\"(.*?)\"", smule).group(1)
            return self.media
        except Exception as e:
            print(e)
            return "Err"

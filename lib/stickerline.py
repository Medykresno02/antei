from requests import get
from bs4 import BeautifulSoup as bs
from json import loads
from re import match
from utilities import jsonify

def sline(req):
    if (url := req.GET.get("url")):
        if (metch := match("(https?://store.line.me/stickershop/product/\d+)", url)):
            eek = stickerLine(metch.group(1)).extract
            return jsonify(eek.to_json, 200) if eek else jsonify({"status": 409, "msg": "Terjadi kesalahan"}, 409)
        else:
            return jsonify({"status": 409, "msg": "url tidak valid"}, 409)
    else:
        return jsonify({"status": 400, "msg": "Parameter url jangan kosong"})

class productLine:
    def __init__(self):
        self.title = None
        self.author = None
        self.thumbnail = None
        self.is_animated = False
        self.price = None
        self.stickers = []

    @property
    def to_json(self):
        self.__dict__.update({"status": 200})
        return self.__dict__

class stickerLine:

    def __init__(self, url:str) -> None:
        """
        url: https://store.line.me/stickershop/product/14903990
        """
        self.url = url
        self.prod = productLine()

    @property
    def extract(self):
        try:
            shop = bs(get(self.url).text, "html.parser")
            stick = [loads(i.get("data-preview")) for i in shop.findAll("li", {"class": "FnStickerPreviewItem"})]
            self.prod.title = shop.find("p", {"data-test": "sticker-name-title"}).text
            self.prod.author = shop.find("a", {"data-test": "sticker-author"}).text
            self.prod.thumbnail = shop.find("img", {"class": "FnImage"}).get("src").split(";c")[0]
            self.prod.is_animated = False if stick[0].get("type") == "static" else True
            self.prod.price = shop.find("p", {"data-test": "sticker-price"}).text
            self.prod.stickers = [i.get(["staticUrl","animationUrl"][self.prod.is_animated]).split(";")[0] for i in stick]
            return self.prod
        except Exception as e:
            print(e)
            return False

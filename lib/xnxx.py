from requests import get
from bs4 import BeautifulSoup as bs
from utilities import jsonify
from urllib.parse import quote
import re, math

def cv_size(size):
    if size == 0:
        return "0 B"
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    return "%s %s" % (round(size / p, 2), ("B","KB","MB","GB","TB")[i])

def xnxx(request):
    if not request.GET.get("url"):return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)
    try:
        html = get(request.GET.get("url")).text
        vid_hd = re.search("setVideoUrlHigh\(\'(.*?)\'\)", html)[1]
        vid_sd = re.search("setVideoUrlLow\(\'(.*?)\'\)", html)[1]
        size_hd = int(get(vid_hd, stream=True).headers.get("content-length"))
        size_sd = int(get(vid_sd, stream=True).headers.get("content-length"))
        return jsonify(
            {
                "status": 200,
                "title": bs(html, "html.parser").find("div", {"class": "clear-infobar"}).strong.text,
                "thumbnail": re.search("setThumbUrl\(\'(.*?)\'", html)[1],
                "description": bs(html, "html.parser").find("p", {"class": "metadata-row video-description"}).text.strip(),
                "duration": bs(html, "html.parser").find("span", {"class": "metadata"}).text.split("-")[0].strip(),
                "views": bs(html, "html.parser").find("span", {"class": "metadata"}).text.split("-")[2].strip(),
                "result": {
                    "hd": {"video": vid_hd, "filesize": cv_size(size_hd)},
                    "sd": {"video": vid_sd, "filesize": cv_size(size_sd)}
                }
            }, 200
        )
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan, mungkin url tidak valid"}, 409)

def search(request):
    
    if not request.GET.get("query"): return jsonify({"status": 400, "msg": "Parameter query jangan kosong"}, 400)
    try:
        anu = bs(get("https://www.xnxx.com/search/%s" % quote(request.GET.get("query"))).text, "html.parser")
    except Exception as e:
        print(e)
        


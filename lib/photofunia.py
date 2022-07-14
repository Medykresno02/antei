from requests import post, get
from bs4 import BeautifulSoup as bs
from utilities import send_file, jsonify

pack = {
    "burnfire": "https://m.photofunia.com/categories/all_effects/burning-fire?server=1",
    "lightning": "https://m.photofunia.com/categories/all_effects/lightning?server=1",
    "sandwrite": "https://m.photofunia.com/categories/all_effects/sand_writing?server=1",
}

def burn_fire(req):
    if not req.GET.get("url"): return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)
    try:
        return send_file(bs(post(pack.get("burnfire"), headers={"User-Agent": "Googlebot"}, files={"image": get(req.GET.get("url")).content}).text, "html.parser").find("div", {"class": "image-container"}).img.get("src"))
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan"}, 409)

def lightning(req):
    if not req.GET.get("url"): return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)
    try:
        return send_file(bs(post(pack.get("lightning"), data={"animated": "animation"}, headers={"User-Agent": "Googlebot"}, files={"image": get(req.GET.get("url")).content}).text, "html.parser").find("div", {"class": "image-container"}).img.get("src"))
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan"}, 409)

def sand_write(req):
    if not req.GET.get("text"): return jsonify({"status": 400, "msg": "Parameter text jangan kosong"}, 400)
    try:
        return send_file(bs(post(pack.get("sandwrite"), data={"text": req.GET.get("text")[:25]}, headers={"User-Agent": "Googlebot"}).text, "html.parser").find("div", {"class": "image-container"}).img.get("src"))
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan"}, 409)

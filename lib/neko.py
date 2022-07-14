from .nekopoi import Hent, Jav
from utilities import jsonify

def hentai(req):
    try:
        hent = Hent(req.GET.get("url")).getto.to_json
        hent.update({"status": 200})
        return jsonify(hent, 200)
    except:
        return jsonify({"status": 409, "msg": "Mungkin url tidak valid"}, 409)

def javv(req):
    try:
        jav = Jav(req.GET.get("url")).getto.to_json
        jav.update({"status": 200})
        return jsonify(jav, 200)
    except:
        return jsonify({"status": 409, "msg": "Mungkin url tidak valid"}, 409)

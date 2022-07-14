from utilities import jsonify
from base64 import *

def enc(req, type: str):
    text = req.GET.get("text")
    try:
        if type == "base16":
            return jsonify({"status": 200, "before": text, "after": b16encode(text.encode()).decode()}, 200)
        elif type == "base32":
            return jsonify({"status": 200, "before": text, "after": b32encode(text.encode()).decode()}, 200)
        elif type == "base64":
            return jsonify({"status": 200, "before": text, "after": b64encode(text.encode()).decode()}, 200)
        elif type == "base85":
            return jsonify({"status": 200, "before": text, "after": b85encode(text.encode()).decode()}, 200)
    except:
        return jsonify({"status": 409, "msg": "Terjadi kesalahan"}, 409)

def dec(req, type: str):
    text = req.GET.get("text")
    try:
        if type == "base16":
            return jsonify({"status": 200, "before": text, "after": b16decode(text).decode()}, 200)
        elif type == "base32":
            return jsonify({"status": 200, "before": text, "after": b32decode(text).decode()}, 200)
        elif type == "base64":
            return jsonify({"status": 200, "before": text, "after": b64decode(text).decode()}, 200)
        elif type == "base85":
            return jsonify({"status": 200, "before": text, "after": b85decode(text).decode()}, 200)
    except:
        return jsonify({"status": 409, "msg": "Enskripsi teks tidak diketahui"}, 409)

from .instagrapi import Client, exceptions
from json import loads
from utilities import jsonify

class Insta:

    def __init__(self):
        self.cl = Client()
        self.is_logged = self.cl.login_by_sessionid("44498574815%3ABa7h5fMMnOUFcC%3A17")

    def profile(self, username):
        if not self.is_logged:
            self.is_logged = self.cl.login("mam_akss","gamtenk.12")
        try:
            info = loads(self.cl.user_info_by_username(username).json())
            info.pop("pk")
            info.update({"status": 200})
            return info
        except exceptions.UserNotFound:
            return False

def profile(req):
    if (user := req.GET.get("username")):
        if (res := Insta().profile(user)):
            return jsonify(res, 200)
        else:
            return jsonify({"status": 409, "msg": "Terjadi kesalahan, pengguna tidak di temukan"}, 409)
    else:
        return jsonify({"status": 400, "msg": "Parameter username jangan kosong"}, 400)

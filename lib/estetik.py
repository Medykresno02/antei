from utilities.file_ import OpenFile, makefile
from .aesthestic.maker import AestheticMaker
from utilities import get_file_json, jsonify, send_file
from io import BytesIO
from requests import get, post
from itertools import cycle
key = cycle(['qRHGsoSSFogajPLzx9ay1Viu','oTUaNbbq5CtUm6jMHFzk3Ziy','3C9qdaMWvRRAi1tAfK4GCzsw','WkRpzF9uRcLX3XKufMn3xCZP','eJunZuzATXmsdwHcZ9AFNrEL','zZVTss2FprPdfrkhdKmZDURb','o1ncjGULb5jFCvwTj1hNs495','e7Gk7GqNx8C6hzwVCTphptBf','JaAvRCVEZLK8wzz1PcpVLj9g','pxVvHW3nsjRywSNLBj8SEnUJ'])

def estetik(req):
    if not req.GET.get("url"): return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)
    try:
        omangko = post('https://api.remove.bg/v1.0/removebg', headers={'X-Api-Key': next(key)}, data={'size': 'auto'}, files={'image_file': get(req.GET.get("url")).content})
        io = BytesIO()
        make = AestheticMaker("src/background.jpg", BytesIO(omangko.content))
        make.create()
        make.background.save(io, "jpeg")
        cr = makefile('wah', io.getvalue())
        #op =OpenFile(cr.unique)
        #js = get_file_json(op, req)
        return send_file(cr.unique)
    except Exception as e:
        print(e)
        return jsonify({"status": 409, "msg": "Terjadi kesalahan, lapor ke admin jika kesalahan terus berlanjut"}, 409)

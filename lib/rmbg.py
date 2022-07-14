from requests import post, get
from utilities import jsonify, get_file_json
from utilities.file_ import makefile
from itertools import cycle
import validators

key = cycle(['qRHGsoSSFogajPLzx9ay1Viu','oTUaNbbq5CtUm6jMHFzk3Ziy','3C9qdaMWvRRAi1tAfK4GCzsw','WkRpzF9uRcLX3XKufMn3xCZP','eJunZuzATXmsdwHcZ9AFNrEL','zZVTss2FprPdfrkhdKmZDURb','o1ncjGULb5jFCvwTj1hNs495','e7Gk7GqNx8C6hzwVCTphptBf','JaAvRCVEZLK8wzz1PcpVLj9g','pxVvHW3nsjRywSNLBj8SEnUJ'])

def remove_bg(request):
    if (url := request.GET.get('url')) or (media := request.FILES.get('image')):
        media: bytes = b''
        if url and validators.url(url):
            media = get(url).content
        elif request.FILES.get('image'):
            media = request.FILES['image'].read()
        if media:
            omangko = post('https://api.remove.bg/v1.0/removebg', headers={'X-Api-Key': next(key)}, data={'size': 'auto'}, files={'image_file': media})
            if omangko.status_code != 200:return jsonify({'status': 409, 'msg': 'Error terjadi kesalahan'}, 406)
            file = makefile('remove_begeh', omangko.content, 60*3)
            return jsonify({'status': 200, **get_file_json(file, request)}, 200)
        else:
            return jsonify({'status': 400, 'msg': 'Url tidak valid'})
    else:
        return jsonify({'status': 400, 'msg': 'Parameter url jangan kosong'}, 400)

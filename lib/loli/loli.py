from utilities import jsonify, get_file_json, send_file
from utilities.file_ import makefile
from json import loads
from requests import get
from random import choice

def Loli(req):
    if req.GET.get('type'):
        try:
            type = req.GET.get('type')
            sfw = loads(open('lib/loli/meki.json', 'r').read())
            nsfw = loads(open('lib/loli/mekis.json', 'r').read())
            if type == 'sfw':
                return send_file(choice(sfw))
                #file = makefile('loli', get(choice(sfw)).content)
                #return jsonify({
                #        'status': 200,
                #        'result': get_file_json(file, req)
                #    }, 200)
            elif type == 'nsfw':
                return send_file(choice(nsfw))
                #file = makefile('loli', get(choice(nsfw)).content)
                #return jsonify({
                #    'status': 200,
                #    'result': get_file_json(file, req)
                #}, 200)
            else:
                return send_file(choice(sfw))
                #file = makefile('loli', get(choice(sfw)).content)
                #return jsonify({
                #    'status': 200,
                #    'result': get_file_json(file, req)
                #}, 200)
        except Exception as e:
            print(e)
            return jsonify({
                'status': 409,
                'msg': 'Terjadi keslahan, silahkan coba lagi, jika kesalahan terus berlanjut tolong lapor ke admin'
            }, 409)
    else:
        return jsonify({
            'status': 400,
            'msg': 'Parameter type jangan kosong'
        }, 400)
        
            

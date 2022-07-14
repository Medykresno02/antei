from saucenao_api import SauceNao as sa
from itertools import cycle
from utilities import jsonify

keys = cycle(['4f10009a6ee01c34a6d4fa8c9369c2d191cc5d4c','dcef15b061477827fa129fe4350bad806acb80a8','bb028172f3a74abac9ee1851465339ca5684b06d','6f833c1ebe9ec52d80237151e1dcaaee8e52eae4','e36b6d1671a38a279acd50f7740de778e552bff0','c39d37cfa86db8041661abeed8d38da3a41b660c','79bba3e994ac236d90780738bed7f34c3717c27f'])
def saus(req) -> dict:
    anu = sa(next(keys))
    if not req.GET.get('url'):return jsonify({'status': 400, 'msg': 'Parameter url jangan kosong'}, 400)
    try:
        _ = anu.from_url(req.GET.get('url')).results[0]
        _.raw.get('data').update(_.raw.get('header'))
        _.raw.get('data').update({'status': 200})
        return jsonify(_.raw.get('data'), 200)
    except Exception as e:
        print(e)
        return jsonify({
            'status': 409,
            'msg': 'Tidak di temukan dalam pencarian'
        }, 409)
    

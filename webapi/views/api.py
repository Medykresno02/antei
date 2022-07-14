"""
Disini tempat func apinya

"""
from typing import Union
import requests
from requests.api import get
from utilities.akun import verify
from django.views.decorators.csrf import csrf_exempt
from utilities.file_ import makefile
from utilities import get_host, jsonify, send_file, download
from lib import saus, infogempa, tiktod, tstalk, blackpink, calc_jodoh, arti_nama, no_hoki, cek_lucky, tafsir_mimpi, remove_bg, cnbc, antara, suara, weather, emoji2img, phgenerate, wattpad, Otakudesu, xnxx, Loli, yta, ytv, yts, tweetS, tweetP, tweetT, tweetTr, smule_dl, ht, webtuun, sline, profile, ttp, attp, enc, dec, hentai, javv, burn_fire, lightning, sand_write, estetik, simi
from lib.twibonizze import Twibbonize
from lib.twibonizze.error import FrameNotFound
from filetype import (guess_mime as mime, guess_extension as ext)
from io import BytesIO
import re
from utilities import get_file_json

def visitor(request):
   return jsonify ({"v":re.search('\"\>([0-9]{1,})\<\/text\>', requests.get("https://visitor-badge.glitch.me/badge?page_id=Anteicodes.Anteiku-API&style=for-the-badge").text).group(1)}, 200)


def testApi(request):
    return jsonify({"status":get_host(request)}, 200)

@csrf_exempt
@verify.verify
def twibon(request):
    params = params = {**({'quality':int(request.GET.get('quality',''))} if request.GET.get('quality','').isnumeric() else {})}
    if not ((request.GET.get('url') or request.FILES.get('image')) and request.GET.get('name')):
        return jsonify({'status':400,'msg':'Parameter '+', '.join({'url','name'} - set(request.GET))+' jangan kosong'}, 400)
    file_ = {'status':True,'content':request.FILES['image'].read()} if request.FILES.get('image') else download(request.GET['url'], 15*1024*1024)
    if not file_['status']:
        return jsonify(file_, 400)
    if mime(file_['content']).split('/')[0] == 'image':
        try:
            im = Twibbonize(request.GET['name']).addToFrame(BytesIO(file_['content']), **params)
            return jsonify({'status':200,**get_file_json(makefile('twibon', im.getvalue()), request)}, 200)
        except FrameNotFound:
            return jsonify({'status':400, 'msg':'nama twibon tidak ditemukan'}, 400)
        except Exception as e:
            print(e)
            return jsonify({'status':406, 'msg':'Masalah tidak diketahui'}, 409)
    else:
        return jsonify({'status':409, 'msg':'url harus berupa gambar'}, 409)

@verify.verify
def p_rnhub(request):
    return phgenerate(request)
@verify.verify
def saucenao(request):
    return saus(request)

@verify.verify
def earthquake(request):
    return infogempa()

@verify.verify
def tikvid(request):
    return tiktod(request)

@verify.verify
def blackp(request):
    return blackpink(request)

@verify.verify
def jodo(request):
    return calc_jodoh(request)

@verify.verify
def artinama(request):
    return arti_nama(request)

@verify.verify
def nohoki(request):
    return no_hoki(request)

@verify.verify
def lucky(request):
    return cek_lucky(request)

@verify.verify
def mimpi(request):
    return tafsir_mimpi(request)

@csrf_exempt
@verify.verify
def rmbg(request):
    return remove_bg(request)

@verify.verify
def cnbceh(request):
    return cnbc(request)

@verify.verify
def antra(request):
    return antara()

@verify.verify
def suare(request):
    return suara()

@verify.verify
def cuaca(request):
    return weather(request)

@verify.verify
def emo2img(request):
    return emoji2img(request)

@verify.verify
def wtpd(request):
    return wattpad(request)

@verify.verify
def otakudes(request):
    return Otakudesu(request)

@verify.verify
def xnx(request):
    return xnxx(request)

@verify.verify
def loli(request):
    return Loli(request)

@verify.verify
def ytaa(request):
    return yta(request)

@verify.verify
def ytvv(request):
    return ytv(request)

@verify.verify
def ytss(request):
    return yts(request)

@verify.verify
def twetS(request):
    return tweetS(request)

@verify.verify
def twetP(request):
    return tweetP(request)

@verify.verify
def twetT(request):
    return tweetT()

@verify.verify
def twetTr(request):
    return tweetTr(request)

@verify.verify
def smule(request):
    return smule_dl(request)

@verify.verify
def htahta(request):
    return ht(request)

@verify.verify
def webton(request):
    return webtuun(request)

@verify.verify
def stline(request):
    return sline(request)

@verify.verify
def igstalk(request):
    return profile(request)

@verify.verify
def tikstalk(request):
    return tstalk(request)

@verify.verify
def ttpp(request):
    return ttp(request)

@verify.verify
def attpp(request):
    return attp(request)

@verify.verify
def b16enc(request):
    return enc(request, "base16")

@verify.verify
def b32enc(request):
    return enc(request, "base32")

@verify.verify
def b64enc(request):
    return enc(request, "base64")

@verify.verify
def b85enc(request):
    return enc(request, "base85")

@verify.verify
def b16dec(request):
    return dec(request, "base16")

@verify.verify
def b32dec(request):
    return dec(request, "base32")

@verify.verify
def b64dec(request):
    return dec(request, "base64")

@verify.verify
def b85dec(request):
    return dec(request, "base85")

@verify.verify
def hent(request):
    return hentai(request)

@verify.verify
def jav(request):
    return javv(request)

@verify.verify
def burnf(request):
    return burn_fire(request)

@verify.verify
def lightn(request):
    return lightning(request)

@verify.verify
def sandw(request):
    return sand_write(request)

@verify.verify
def estik(request):
    return estetik(request)

@verify.verify
def simih(request):
    return simi(request)

def sendF(request, result):
    return send_file(result, 'result')

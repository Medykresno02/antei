from django.http import HttpResponse, HttpResponseNotFound
from utilities.file_ import OpenFile, File, listdir
from json import dumps
from filetype import guess_mime as mime, guess_extension as ext
from requests import get
import requests
from urllib.parse import quote
import math, os, validators
from socket import inet_aton, inet_ntoa
from struct import pack, unpack
from random import randint

def jsonToParameter(json):
    return "&".join(map(lambda x:f"{x}={quote(json[x])}", json))

def get_file_json(file:File, req):
    return {'filename':file.filename, 'mime':file.mime, 'ext':file.ext, 'expired':file.expired, 'filesize':file.size, 'filesize_s':sizeFile(file.size), 'url':get_host(req)+'/result/'+file.unique}

def get_host(req):
    return f"{'http' if req.META['SERVER_NAME']=='localhost' else 'https'}://{req.get_host()}"

def gen_ipv4():
    a = unpack("!L", inet_aton("39.192.0.0"))[0]
    b = a | (0xffffffff >> 10)
    return str(inet_ntoa(pack("!L", randint(a, b))))

def jsonify(obj, status=None):
    rv = dumps(obj, indent=4, separators=(', ',': '))
    return HttpResponse(f'{rv}\n', content_type='application/json') if not status else HttpResponse(f'{rv}\n', content_type='application/json', status=status)

def download(url, max_length=1024*1024):
    try:
        binary=b''
        r = requests.get(url, stream=True)
        if r.headers.get('Length-Content', 0) > max_length:
            return {'status':False, 'msg':'ukuran file melebihi batas maksimal'}
        for i in r.iter_content(1024):
            binary+=i
            if binary.__len__()>max_length:
                return {'status':False, 'msg':'ukuran file melebihi batas maksimal'}
        return {'status':True, 'content':binary}
    except Exception:
        return {'status':False, 'msg':'URL tidak valid'}


def send_file(fp, path=None):
    """
    fp: Filename/url/bytes
    path: FilePath/Dir
    """
    try:
        print(f'download :{fp}')
        file = OpenFile(fp)
        if validators.url(fp):
            buff = get(fp).content
            resp = HttpResponse(buff, content_type=mime(buff), status=200)
        elif file.binary:
            resp = HttpResponse(file.binary, content_type=file.mime, status=200)
        else:
            resp = HttpResponseNotFound("<h1>File tidak ada atau sudah di hapus</h1>")
        return resp
    except Exception as e:
        print(e)
        return HttpResponseNotFound("<h1>File tidak ada atau sudah di hapus</h1>")

def h2k(num:int):
    if num == 0:return '0'
    size_name=["","K","M","G","T","P","E","Z","Y"]
    i = int(math.floor(math.log(num, 1000)))
    p = math.pow(1000, i)
    s = round(num / p, 2)
    anu = "%s %s" % (s, size_name[i])
    if anu.strip().endswith('.0'):
        return anu.strip()[:-2]
    return anu.strip()

def sizeFile(num):
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def get_ip(request):
    ip_private = request.META.get('REMOTE_ADDR', '')
    ip_publik = request.META.get('HTTP_X_FORWARDED_FOR', ip_private)
    return ip_publik if not ',' in ip_publik else ip_publik.split(',')[0].strip()

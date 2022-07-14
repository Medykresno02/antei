from random import choice, randint, random
from os import listdir, path, remove
import math, subprocess
from requests import post
from glob import glob
from base64 import b64encode as bb
from utilities import send_file, jsonify

def imgUploader(base64_):
    '''
    base64_ : String base64.encode
    '''
    f=post("https://api.imgbb.com/1/upload?expiration=216000&key=baa46cea79544c4942a4b3d2d21be87c", data={"image":base64_})
    if f.status_code == 200:
        return f.json()["data"]["url"]
    else:
        return "Upload Gambar Gagal"

def ht(req):
    if (text := req.GET.get("text")):
        img = choice(glob('./**/Aest*', recursive=True))
        font = 'src/Roboto-Black.ttf'
        w = 1024
        h = w
        s = str(w) + 'x' + str(h)
        xF = f"({noise('X', 2, w, 1)}+{noise('Y', 1, h, 1)})/2+128"
        yF = "((%s%s*%s(X/%s*4*PI))+%s+%s)/1.7+128" % (choice(['','-']), 45 * w / 2048, choice(['sin','cos']), w, noise('X', 5, w, 0.8), noise('Y', 2, h, 1))
        fsize = 320 / 2048 * w
        lh = 1.5
        _format = ',format=rgb24'
        hiji = f'(h-text_h)/2-(text_h*{lh})'
        dua = f'(h-text_h)/2+(text_h*{lh})'
        text = text[:10]
        layers = [
            f'[v:0]scale={s}{_format}[im]',
            textArg('HARTA', 'black', 'white', fsize, font, '(w-text_w)/2', hiji, w, h) + _format + '[top]',
            textArg('TAHTA', 'black', 'white', fsize, font, '(w-text_w)/2', '(h-text_h)/2', w, h) + _format + '[mid]',
            textArg(text, 'black', 'white', fsize, font, '(w-text_w)/2', dua, w, h) + _format + '[bot]',
            '[top][mid]blend=all_mode=addition[con]',
            '[con][bot]blend=all_mode=addition[txt]',
            f"nullsrc=s={s},geq='r={xF}:g={xF}:b={xF}'[dx]",
            f"nullsrc=s={s},geq='r={yF}:g={yF}:b={yF}'[dy]",
            '[txt][dx][dy]displace[wa]',
            '[im][wa]blend=all_mode=multiply:all_opacity=1'
        ]
        o = str(random())+'.jpg'
        argz = [
            './bin/ffmpeg',
            '-y',
            '-i', img,
            '-filter_complex', ';'.join(layers),
            '-frames:v', '1',
            o
        ]
        print(argz)
        subprocess.call(argz)
        if path.exists(o):
            voss = bb(open(o, 'rb').read())
            remove(o)
            return send_file(imgUploader(voss))
        else:
            return jsonify({"status": 409, "msg": "Terjadi kesalahan!. jika kesalahan terus berlanjut, mohon lapor ke admin"})
    else:
        return jsonify({"status": 400, "msg": "Parameter text jangan kosong"}, 400)

def textArg(text, bg, color, size, fontfile, x = '200', y = '200', w = 1024, h = 1024):
    text = text.replace('\\', '\\$&')
    return f"color={bg}:s={w}x{h},drawtext=text='{text}':fontfile='{fontfile}':x={x}:y={y}:fontsize={size}:fontcolor={color}"

def toFixed(num, num2):
    return round(int(num), int(num2))

def rand(min, max, q = 0.001):
    return math.floor((random() * (max - min)) / q) * q

def formu(var, freq, offset, amp, add):
    return f'({toFixed(add, 3)}+{toFixed(amp, 4)}*sin({toFixed(offset, 6)}+2*PI*{var}*{toFixed(freq, 6)}))'

def noise(var, depth = 4, s = 1024, freq = None):
    form = []
    for i in range(depth):
        form.append(
            formu(
                var,
                freq * rand(40, 80) * (s / 2048) / s * ((i + 1) / 5),
                rand(-math.pi, math.pi),
                (i + 1) / depth * 8,
                0
            )
        )
    return '+'.join(form)

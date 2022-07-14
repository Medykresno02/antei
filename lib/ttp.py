from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from random import randint
from itertools import chain
from utilities import send_file, jsonify
from utilities.file_ import makefile
from io import BytesIO

def ttod(text:str, color="white"):
    R, G, B = (randint(0,256) for _ in range(3))
    wrep = list(chain.from_iterable([wrap(i, width=10) for i in text.splitlines()[:5] if i != ""]))
    text = "\n".join(wrep)
    img = Image.new("RGBA", (512, 512), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("src/cocok.ttf", size=126)
    TinggiText=[(font.getsize(i)[1])for i in text.split("\n")]
    jum=sum(TinggiText)+len(text.split("\n"))-70
    awal=(img.height/2)-(jum/2)
    outlineRange = int(font.size/15)
    for x in text.splitlines():
        for y in range(-outlineRange, outlineRange+1):
            for z in range(-outlineRange, outlineRange+1):
                draw.text(
                    (int(img.width/2)-(font.getsize(x)[0]/2)+5, awal+5),
                    x, fill="black", font=font
                )
        draw.text(
            (int(img.width/2)-(font.getsize(x)[0]/2), awal),
            x, fill=color or (R, G, B), font=font
        )
        awal+=100
    return img

def attp(req):
    if (text := req.GET.get("text")):
        anu = [ttod(text, None) for i in range(10)]
        byte = BytesIO()
        anu[0].save(byte, format="WEBP", save_all=True, append_images=anu[1:], duration=100, loop=0, transparency=0, optimize=False)
        return send_file(makefile("attp.webp", byte.getvalue()).unique)
    else:
        return jsonify({"status": 400, "msg": "Parameter text jangan kosong"}, 400)

def ttp(req):
    if (text := req.GET.get("text")):
        byte = BytesIO()
        ttod(text).save(byte, format="PNG", optimize=False)
        return send_file(makefile("ttp.png", byte.getvalue()).unique)
    else:
        return jsonify({"status": 400, "msg": "Parameter text jangan kosong"}, 400)

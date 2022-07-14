from requests import get
from bs4 import BeautifulSoup as bs
from utilities import jsonify

def infogempa():
    beemkage = bs(get('https://warning.bmkg.go.id').text, 'html.parser')
    lindu = beemkage.findAll('li')
    info = beemkage.findAll('p')[:-1]
    return jsonify({
        'status': 200,
        'magnitudo': list(lindu[0].strings)[0],
        'kedalaman': list(lindu[1].strings)[0],
        'koordinat': ' - '.join(list(lindu[2].strings)),
        'lokasi': list(info[0].strings)[1],
        'wilayah': ' '.join(list(info[1].strings)),
        'arahan': list(info[2].strings)[1],
        'saran': list(info[3].strings)[1],
        'shakemap': info[4].a.get('href')
    }, 200)

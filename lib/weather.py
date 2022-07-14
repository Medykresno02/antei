from requests import get
from utilities import jsonify

def degree_celsius(temp):
    return str(round(float(temp) - 273.15, 2))

def weather(req, lang='en'):
    if (req.GET.get('city')):
        try:
            key = '5cc1946f62646c49e5b50d0246d51732'
            anu = get('http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s' % (city, key)).json()
            return jsonify({'status': 200, 'cc': anu['sys']['country'], 'coordinate': 'Lon : %s\nLat : %s' % (str(anu['coord']['lon']), str(anu['coord']['lat'])), 'temp_kelvin': '%s K' % str(anu['main']['temp']), 'temp_celcius': '%s° C' % degree_celsius(anu['main']['temp']), 'pressure': '%s Pa' % str(anu['main']['pressure']), 'humidity': '%s' % str(anu['main']['humidity']) + ' %', 'cityname': anu['name']}, 200)
        except Exception as e:
            print(e)
            return jsonify({'status': 409, 'msg': 'Terjadi kesalagan, mungkin kota tidak terdaftar pada database'}, 409)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter city jangan kosong'}, 400)

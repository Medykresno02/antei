from requests import post, get
from bs4 import BeautifulSoup as bs
from utilities import jsonify
from utilities.file_ import makefile
from urllib.parse import quote
from html2text import html2text
from re import search, findall

def calc_jodoh(request):
    if (nama := request.GET.get('n1')):
        if (nama2 := request.GET.get('n2')):
            anu = bs(post(f"https://www.primbon.com/kecocokan_nama_pasangan.php?nama1={quote(nama)}&nama2={quote(nama2)}&proses=+Submit%21+").text, 'html.parser')
            info = anu.find("div", {"id": "body"})
            lis = list(info.strings)[5::][:-33]
            file = makefile("primbon", get(f"https://www.primbon.com/{info.img['src']}").content, 60*2)
            return jsonify({'status': 200, 'nama_anda': lis[0].strip(), 'nama_pasangan': lis[2].strip(), 'sisi_positif': lis[4].strip(), 'sisi_negatif': lis[6].strip(), 'catatan': lis[7], 'gambar': f"{'http' if request.META['SERVER_NAME']=='localhost' else 'https'}://{request.get_host()}/result/{file.unique}"}, 200)
        else:
            return jsonify({'status': 400, 'msg': 'Parameter n2 jangan kosong'}, 400)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter n1 jangan kosong'})

def arti_nama(request):
    if (nama := request.GET.get('nama')):
        anu = bs(post(f"https://www.primbon.com/arti_nama.php?nama1={quote(nama)}&proses=+Submit%21+").text, 'html.parser')
        return jsonify({'status': 200, 'nama': anu.i.next, 'arti': anu.i.next.next.split(':')[1].strip()}, 200)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter nama jangan kosong'}, 400)

def no_hoki(request):
    if (nomor := request.GET.get('nohp')):
        anu = post('https://www.primbon.com/no_hoki_bagua_shuzi.php', data={'nomer': nomor, 'submit': ' Submit! '}).text
        if 'ERROR!' in anu:return jsonify({'status': 409, 'msg': 'error nomor tidak valid'}, 409)
        all_ = findall('= (.*?)<br>', anu)
        return jsonify({'status': 200, 'nohp': search('<b>No. HP : (.*?)</b>', anu).group(1), 'percent_angka_shuzi': search('<b>% Angka Bagua Shuzi : (.*?)</b>', anu).group(1).replace('&#37','%'), 'energi_positif': {'kekayaan': all_[0], 'kesehatan': all_[1], 'cinta': all_[2], 'kestabilan': all_[3], 'total': all_[4].replace('&#37</b>','%')}, 'energi_negatif': {'perselisihan': all_[5], 'kehilangan': all_[6], 'malapetaka': all_[7], 'kehancuran': all_[8], 'total': all_[9].replace('&#37</b>','%')}, 'note': bs(anu, 'html.parser').i.text.strip()}, 200)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter nohp jangan kosong'}, 400)

def cek_lucky(request):
    if (nama := request.GET.get('nama')):
        if (tgl := request.GET.get('tgl')):
            if (bln := request.GET.get('bln')):
                if (thn := request.GET.get('thn')):
                    try:
                        anu = post('https://www.primbon.com/potensi_keberuntungan.php', data={'nama': nama, 'tanggal': tgl, 'bulan': bln, 'tahun': thn, 'submit': '+Submit!+'}).text
                        return jsonify({'status': 200, 'nama': nama, 'note': search('(Se.*?)<br>', anu).group(1), 'hasil': bs(anu, 'html.parser').i.text}, 200)
                    except Exception as e:
                        print(e)
                        return jsonify({'status': 409, 'msg': 'Error mungkin isi parameter tidak valid'}, 409)
                else:
                    return jsonify({'status': 400, 'msg': 'Parameter thn jangan kosong'}, 400)
            else:
                return jsonify({'status': 400, 'msg': 'Parameter bln jangan kosong'}, 400)
        else:
            return jsonify({'status': 400, 'msg': 'Parameter tgl jangan kosong'}, 400)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter nama jangan kosong'}, 400)

def tafsir_mimpi(request):
    if (q := request.GET.get('q')):
        try:
            anu = post(f'https://www.primbon.com/tafsir_mimpi.php?mimpi={quote(q)}&submit=+Submit+').text
            if 'Tidak ditemukan' in anu:return jsonify({'status': 409, 'msg': f'Error tafsir mimpi {q} tidak di temukan'}, 409)
            hasil = [f'{[bs(_.split("<br><br>")[1], "html.parser").text for _ in findall("(.*?) =", anu)[4::][:-3]][__[0]]} = {search(findall("(.*?) =", anu)[4::][:-3][__[0]]+" = (.*?)<br>", anu).group(1)}' for __ in enumerate([bs(_.split('<br><br>')[1], 'html.parser').text for _ in findall("(.*?) =", anu)[4::][:-3]])]
            hasil = [html2text(i).strip() for i in hasil]
            return jsonify({'status': 200, 'hasil': hasil, 'total': len(hasil)}, 200) if len(hasil) > 1 else jsonify({'status': 200, 'hasil': hasil[0], 'total': len(hasil)}, 200)
        except Exception as e:
            print(e)
            return jsonify({'status': 409, 'msg': f'Error tafsir mimpi {q} tidak di temukan'}, 409)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter q jangan kosong'}, 400)

import secrets
from twilio.rest import Client
import requests
from webapi.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.http import JsonResponse
from utilities.akun import AccessToken, encrypt_decrypt, enkripsi, login_kuki, account, verify, getDokumentasi
from ..models import Dokumentasi, CodeDocumentation, Session
from utilities.email_sender import kirim_verifikasi
from utilities import get_ip, jsonToParameter, get_host
from django.shortcuts import render, redirect
from requests import get
from random import choice
from utilities.Action import createAction
from multicolorcaptcha import CaptchaGenerator as cp;capt=cp(10)
from io import BytesIO
from base64 import b64encode
rand = ["text-warning","text-danger","text-info","text-success","text-primary"]
@verify.docs_decorator
def dokumentasi(request, path=None, session:Session=Session):
    if path == None:
        return redirect("/")
    docs_data = Dokumentasi.objects.filter(url_dokumentasi=path)
    if docs_data:
        docs_data=docs_data.first()
        #user=session.user
        data = {"title":docs_data.title, "title_panel":docs_data.title_panel, "example_ajax":docs_data.example_ajax, "code":[], "path_api":docs_data.path_api}
        for docs in CodeDocumentation.objects.filter(api_name=docs_data):
            data["code"].append({"language":docs.language, "language_code":docs.language_code,"code":re.sub('(https?://.*?\.herokuapp\.com|%url%)', get_host(request), re.sub('(%mpikey%|mpikey)',session.user.apikey if session else "Login dulu beb:*", docs.code))}) #kalo masih kurang tinggal tambah sendiri:)
        data.update({"keys":list(data["example_ajax"]), 'host': f"{'http' if request.META['SERVER_NAME']=='localhost' else 'https'}://{request.get_host()}"})
        data.update({"params":jsonToParameter(data["example_ajax"]), "apikey":session.user.apikey if session else "Login dulu beb:*", "AccessToken":encrypt_decrypt()._encrypt(session.AccessToken) if session else None, "avatar":session.user.picture if session else "https://avatars.githubusercontent.com/u/86209322", "nama":session.user.nama if session else "demo","limit": session.user.max_request if session else 0,"kategori": enumerate(getDokumentasi()), "color": rand})
        return render(request, "docs.html", data)
    return redirect("/")


@csrf_exempt
def ip_api(request):
    action = request.POST.get("action")
    ip     = request.POST.get("ip")
    AccessToken_   = request.POST.get("AccessToken")
    if action and ip and AccessToken:
        user_=AccessToken(AccessToken_)
        if user_.get:
            user:User=user_.get.user
            if action == "add":
                if json.loads(user.allow_ip).__len__() < user.max_ip: # max 10 ip yg untuk 1 akun
                    print('ip masih dibawah 10')
                    ses=user_.get
                    ses.Action.append(createAction.ip_allow('add',ip))
                    ses.save()
                    return JsonResponse({"status":user_.setIP(ip)})
                else:
                    return JsonResponse({"status":False, "msg":"Jumlah IP telah terlampaui"})
                
            elif action == "remove":
                ses = user_.get
                ses.Action.append(createAction.ip_allow('delete',ip))
                ses.save()
                return JsonResponse({"status":user_.rmIP(ip)})
        else:
            return JsonResponse({"status":False, "msg":"Akun Tidak Terdaftar"})
    return JsonResponse ({"status":False, "msg":"Format Salah"})

@verify.kuki
def dashboard(request, session:Session):
    if session:
        user = session.user
        print(f"REMOTE_HOST: {request.META['REMOTE_HOST']}")
        print(f"SERVER_NAME: {request.META['SERVER_NAME']}")
        print(f"HTTP_HOST: {request.META['HTTP_HOST']}")
        print(f"IP_PUBLIK: {request.META.get('HTTP_X_FORWARDED_FOR','')}")
        return render(request, "dashboard.html", {"AccessToken":encrypt_decrypt()._encrypt(session.AccessToken),"nama":user.nama, "apikey":user.apikey, "hit":user.req_counter, "max_hit":user.max_request, "allow_ip":user.allow_ip, "max_ip": user.max_ip,"limit": user.max_request, "avatar":user.picture, "kategori": enumerate(getDokumentasi()), "color": rand})
    else:
        return redirect("/login")

@verify.kuki
def page_ip(request, session:Session):
    if session:
        user = session.user
        return render(request, "ip.html", {"AccessToken":encrypt_decrypt()._encrypt(session.AccessToken),"nama":user.nama,  "avatar":user.picture, "allow_ip":user.allow_ip,"ip_private":request.META["REMOTE_ADDR"], "limit":user.max_request, "kategori": enumerate(getDokumentasi()), "color": rand})
    else:
        return redirect("/login")

def signup(request):
    captcha = capt.gen_math_captcha_image(3, True, margin=False)
    image = BytesIO()
    captcha.get('image').save(image, format="PNG")
    nama = request.POST.get("nama")
    hp = re.sub(r'^(\+?62)','0',request.POST.get("hp",""))
    email = request.POST.get("email")
    password = request.POST.get("password")
    method = request.POST.get('vmethod')
    jawaban = request.POST.get("jawaban")
    if nama and email and hp and password and method and jawaban:
        print('after if')
        if request.session.get('session'):
            print('session check')
            token=encrypt_decrypt().decrypt(request.session['session'].encode()).decode()
            us=User.objects.filter(verified_token=token, email_verfied=False).first()
            print(token)
            if us:
                print('delete')
                us.delete()
            else:
                request.session.pop('session','')
                request.session.pop('password','')
        create = account(email=email, password=password, no_hp=hp)
        session = {'nama':nama, 'email':email,'hp':hp, 'password':password, 'vmethod':method, 'session':True}
        ctx = create.login_without_verified
        jwaban = request.session.pop('equation_result')
        request.session['equation_result'] = captcha.get('equation_result')
        session.update({"captcha_img":b64encode(image.getvalue()).decode()})
        stat = create.signup(nama, get(f"https://waifu.pics/api/sfw/{choice(['waifu','neko'])}").json()['url'])
        if stat == True:
            ctx = create.login_without_verified
            request.session['session'] = encrypt_decrypt().encrypt(ctx.verified_token.encode()).decode()
            request.session['password'] = encrypt_decrypt().encrypt(password.encode()).decode()
            host = f"{'http://' if request.get_host() in ['localhost:8000','127.0.0.1:8000'] else 'https://'}{request.get_host()}"
            url =  f"{host}/verification/{ctx.verified_token}"
            if jwaban != jawaban:
                return render(request, "signup.html", {"msg":"Captcha salah",**session})
            if method == 'email':
                print(url)
                kirim_verifikasi(email,url)
                return render(request, "signup.html", {"msg":"Method Rusak"})
            elif method == 'whatsapp':
                stat=requests.post("http://message.naufalhosting.org/api/v2/wa/sendSpecialButtons", headers = {'Content-Type':'application/json','Authorization':'Bearer anteicodes|FVlzFMmkdSuZZQUKMbtfSsOYIkLtpZpbQvPWGo'}, json = {'number': hp, 'title': f'Hai, {ctx.nama}', 'message': '*Klik Verification untuk mengunjungi link verifikasi*', 'footer': 'Anteicodes', 'buttons':  [{"type": "url", "text": "Verification", "url": url}]})
                if not stat.json()['status'] == True:
                    ctx.delete()
                    return render(request, "signup.html", {"msg":"Terjadi kesalahaan saat mengirim link verifikasi", **session})
                return render(request, "signup.html", {"terkirim":"Link Verifikasi terkirim silahkan cek chat whatsapp anda",**session})
            elif method == "twilio":
                try:
                    client=Client('AC00928dbeb8f3f07b1e11067f00c0e1bb','103a30b27b8b37d07b21a8c33efba96e')
                    print('whatsapp:+'+re.sub(r'^0', '62', hp))
                    client.messages.create(body=f'Klik link di bawah ini untuk melakukan verifikasi terhadap akun anda *{ctx.nama}*\n https://antei.codes/verification/{ctx.verified_token}', from_= 'whatsapp:+14155238886', to='whatsapp:+'+re.sub(r'^0', '62', hp))
                    return render(request, "signup.html", {"terkirim":"Link Verifikasi terkirim silahkan cek chat whatsapp anda",**session})
                except Exception:
                     return render(request, "signup.html", {"msg":"Pastikan Nomer anda benar", **session})
            else:
                return render(request, "signup.html", {"msg":"Method tidak ditemukan", **session})
        else:
            return render(request, "signup.html", {'msg':stat, **session})
    elif request.session.get('password') and request.session.get('session'):
        data: User = User.objects.filter(verified_token=encrypt_decrypt().decrypt(request.session['session'].encode()).decode())
        nama     = data.nama
        email    = data.email
        hp       = data.phone_number
        password = encrypt_decrypt().decrypt(request.session['password'].encode()).decode()
        method   = 'whatsapp'
        img_base64 = b64encode(image.getvalue()).decode()
        request.session['equation_result'] = captcha['equation_result']
        return render(request, "signup.html", {'nama':nama, 'email':email,'hp':hp, 'password':password, 'vmethod':method, 'session':True,'captcha_img':img_base64})
    img_base64 = b64encode(image.getvalue()).decode()
    request.session['equation_result'] = captcha['equation_result']
    return render(request, "signup.html", {"captcha_img":img_base64})


@verify.kuki
def logOut(request,session):
    resp=redirect("/login")
    session.delete()
    resp.delete_cookie("XxFgsT")
    return resp

def verified(request, token=None):
    validity = User.objects.filter(verified_token=token)
    if validity and token:
        user = validity.first()
        user.email_verfied = True
        user.save()
        resp = redirect("/login")
        request.session["action"] = {"success":"berhasil diverifikasi silahkan login ulang"}
    else:
        request.session["action"]  = {"msg":"verifikasi gagal"}
    return redirect("/login")

def login(request):
    email = request.POST.get("email","")
    password = request.POST.get("password")
    if email and password:
        em = {'no_hp':re.sub(r'^(\+?62)','0',email)} if email.isnumeric() else {'email':email}
        user = account(**em, password=password).login
        if user:
            kuki=secrets.token_hex(86)
            new_session = Session(user=user, ua=request.META.get('HTTP_USER_AGENT','Unknown'), ip=get_ip(request), cookie_value=enkripsi(kuki).encrypt, AccessToken=secrets.token_hex(64), Action=[])
            new_session.save()
            resp = redirect("/")
            resp.set_cookie("XxFgsT", kuki)
            return resp
        else:
            return render(request, "signin.html", {"msg":"Email & Password Salah"})
    elif request.COOKIES.get("XxFgsT"):
        return redirect("/")
    return render(request, "signin.html", request.session.pop('action', {}))

@verify.kuki
def index(request, session:Session):
    if session:
        user = session.user
        resp = {"AccessToken":encrypt_decrypt()._encrypt(session.AccessToken),"nama":user.nama,"avatar":user.picture,"limit":user.max_request,"apikey":user.apikey}
        if not user.email_verfied:
            resp.update({"msg": "Verifikasi email terlebih dahulu!"})
        resp.update({"msg": "Selamat datang %s" % user.nama, "kategori": enumerate(getDokumentasi()), "color": rand})
        if len(json.loads(user.allow_ip)) < user.max_ip:
            login_kuki(request.COOKIES['XxFgsT']).setIP(request.META.get('HTTP_X_FORWARDED_FOR','127.0.0.1'))
        return render(request, 'home.html', resp)
    else:
        resp = {"avatar": "https://avatars.githubusercontent.com/u/86209322", "nama": "demo", "limit": 0, "apikey": "Login dulu bep:*", "kategori": enumerate(getDokumentasi()), "msg": "Silahkan login jika ingin mencoba fitur yang tersedia pada website api ini", "color": rand}
        return render(request, 'home.html', resp)

@verify.kuki
def contacts(request, session:Session):
    if session:
        user = session.user
        resp = {"AccessToken":encrypt_decrypt()._encrypt(session.AccessToken),"nama":user.nama,"avatar":user.picture,"limit":user.max_request,"color":rand,"kategori": enumerate(getDokumentasi())}
    else:
        resp = {"nama": "demo", "apikey": "Login dulu beb:*", "avatar": "https://avatars.githubusercontent.com/u/86209322","limit":0,"color": rand,"kategori": enumerate(getDokumentasi())}
    return render(request, "contacts.html", resp)

@csrf_exempt
def userInfo(request):
    if request.POST.get("AccessToken"):
        user = AccessToken(request.POST['AccessToken']).get.user
        if user:
            return JsonResponse({
                "nama":user.nama,
                "picture":user.picture,
                "apikey":user.apikey,
                "hit":user.req_counter,
                "max_hit":user.max_request,
                "allow_ip":json.loads(user.allow_ip)
            })
        else:
            return JsonResponse({})
    else:
        return JsonResponse({})

@csrf_exempt
def resetapikey(request):
    if request.POST.get("AccessToken"):
        session = AccessToken(request.POST["AccessToken"])
        ses = session.get
        if ses:
            ses.Action.append(createAction.reset_apikey())
            ses.save()
            return JsonResponse({"apikey":session.reset_apikey})
    return JsonResponse({"apikey":False})

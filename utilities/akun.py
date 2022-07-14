from django.db.models import Q
from cryptography.fernet import Fernet
from typing import Union
import datetime
from secrets import token_hex, token_urlsafe
from utilities.ipmatcher import match, matchForSetIP
from utilities import jsonify, get_ip
from webapi.models import User, DokumentasiKategori, Dokumentasi, Session
from django.utils import timezone
#from crypt import crypt
from bcrypt import hashpw
from AnteikuAPI.settings import BCRYPT_KEY#SECRET_KEY
import json
from django.shortcuts import redirect
class EmailOrPhoneNumberInvalid(Exception):
    pass
def getDokumentasi():
    result = []
    for i in DokumentasiKategori.objects.all():
        dataD = {"name":i.name, "icon":i.icon, "child":[]}
        for x in Dokumentasi.objects.filter(categori=i):
            dataD["child"].append({"name":x.title, "icon":x.icon, "url":x.url_dokumentasi})
        result.append(dataD)
    return result

class verify:
    @staticmethod
    def verify(f):
        def check(request):
            if request.headers.get("Authorization"):
                user = apikey(request.headers.get("Authorization"))
                if user.isValid:
                    if not user.ipvalidity(get_ip(request)):
                        return jsonify({"msg":"Akses Ditolak", "status": 403}, 403)
                    if user.Add:
                        return f(request)
                    else:
                        return jsonify({"msg":"request telah mencapai batas", "status": 402}, 402)
                else:
                    return jsonify({"msg":"apikey tidak valid", "status": 405}, 405)
            else:
                return jsonify({"msg":"Tolong atur apikey pada headers anda", "status": 407}, 407)
        return check
    
    @staticmethod
    def kuki(f):
        def check(request):
            if request.COOKIES.get("XxFgsT"):
                kuki = request.COOKIES["XxFgsT"]
                session = login_kuki(kuki).get
                if session:
                    return f(request, session)
                else:
                    #return f(request, None)
                    resp=redirect("/")
                    resp.delete_cookie("XxFgsT")
                    return resp
            return f(request, None)
        return check
    
    @staticmethod
    def docs_decorator(f):
        def check(request,path=None):
            if request.COOKIES.get("XxFgsT"):
                kuki = request.COOKIES["XxFgsT"]
                session = login_kuki(kuki).get
                if session:
                    return f(request=request,path=path,session=session)
                else:
                    #resp=redirect("/login")
                    #resp.delete_cookie("XxFgsT")
                    #return resp
                    return f(request=request,path=path,session=None)
            #return redirect("/login")
            return f(request=request,path=path,session=None)
        return check


class enkripsi:
    def __init__(self, key) -> None:
        self.key:str = key
    
    @property
    def encrypt(self):
        #return crypt(self.key, SECRET_KEY)
        return hashpw(self.key.encode(), BCRYPT_KEY).decode()

class encrypt_decrypt(Fernet):
    def __init__(self) -> None:
        super().__init__(b'spaY9tHLa1g2AE5XxvqTcSCxHFlVkArG3_m9NqPjKUE=')
    def _encrypt(self, text:Union[str, bytes])->str:
        return self.encrypt(text.encode() if isinstance(text, str) else text).decode()
    def _decrypt(self, text:Union[str, bytes])->str:
        return self.decrypt(text.encode() if isinstance(text, str) else text).decode()

class apikey:
    def __init__(self, apikey) -> None:
        self.apikey = apikey

    @property
    def isValid(self)->User:
        return User.objects.filter(apikey=self.apikey).first()
    @property
    def limitCheck(self)->Union[bool, User]:
        user = self.isValid
        if not user.plan_name == "TRIAL" and user.expired < timezone.now():
            user.req_counter = 0 
            user.max_request = 0
            user.save()
            return False 
        if user:
            return user if user.req_counter < user.max_request else False
        return False


    def ipvalidity(self, ip):
        user = self.isValid
        if user:
            return match(json.loads(user.allow_ip), ip)
        else:
            False

    @property
    def Add(self):
        user = self.limitCheck
        if not isinstance(user, bool):
            user.req_counter+=1
            user.save()
            return True
        else:
            return False
             

class account:
    def __init__(self, password: str, email: str='', no_hp: str=''):
        if email and no_hp:
            self.email_pn = {'phone_number': no_hp, 'email':email}
        elif no_hp:
            self.email_pn = {'phone_number':no_hp}
        elif email:
            self.email_pn = {'email':email}
        else:
            raise EmailOrPhoneNumberInvalid()
        self.enc = enkripsi(password)

    @property
    def login(self)->Union[User, bool]:
        if (u := User.objects.filter(**self.email_pn).first()):
            return User.objects.filter(**self.email_pn, password=self.enc.encrypt, email_verfied=True).first() if u.email_verfied else User.objects.filter(**self.email_pn, password=self.enc.encrypt, email_verfied=False).first()
        else:
            return False

    @property
    def login_without_verified(self)->User:
        user = User.objects.filter(**self.email_pn, password=self.enc.encrypt, email_verfied=False).first()
        return user

    def signup(self, nama, profile)->Union[str, bool]:
        if nama.__len__() < 5 and self.enc.key.__len__() < 5:
            return False
        elif User.objects.filter(Q(email=self.email_pn['email'])|Q(phone_number=self.email_pn['phone_number'])).first():
            return "Email"
        User(nama=nama, **self.email_pn, email_verfied=False, picture=profile, password=self.enc.encrypt, verified_token=token_hex(64), apikey=token_urlsafe(32), plan_name="TRIAL", max_request=120, allow_ip="[]", max_ip=3, req_counter=0, expired=timezone.now()+datetime.timedelta(days=30)).save()
        return True

    @property
    def delete(self):
        user = self.login
        if user and not isinstance(user, bool):
            user.delete()
            return True
        else:
            return False



class login_kuki(enkripsi):
    def __init__(self, kuki) -> None:
        super().__init__(kuki)
    
    def isIP(self, ip: list):
        return list(filter(lambda x:not matchForSetIP(x), ip))

    def setIPs(self, ip:list):
        ipl = self.isIP(ip)
        if ipl:
            return ipl
        else:
            user=self.get
            user.allow_ip = json.dumps(ip)
            user.save()
            return True
    
    def setIP(self, ip):
        if matchForSetIP(ip):
            user = self.get.user
            if ip in json.loads(user.allow_ip):
                return False
            user.allow_ip = json.dumps(json.loads(user.allow_ip)+[ip])
            user.save()
            return True
        else:
            return False

    def rmIP(self, ip):
        session = self.get
        ips = json.loads(session.user.allow_ip)
        if ip in ips:
            user=session.user
            ips.remove(ip)
            user.allow_ip = json.dumps(ips)
            user.save()
            return True
        else:
            return False

    @property
    def get(self)->Session:
        session = Session.objects.filter(cookie_value=self.encrypt).first()
        if session:
            return session
        return session

    @property
    def reset_apikey(self)->str:
        session=self.get
        if session:
            user=session.user
            user.apikey = token_urlsafe(32)
            user.save()
            return user.apikey
        else:
            return ""

    @property
    def logOut(self)->bool:
        session=Session.objects.filter(cookie_value=self.encrypt)
        if session:
            session.delete()
            return True
        else:
            return False

class AccessToken():
    def __init__(self, AT:Union[bytes, str], dec:bool=True) -> None:
        self.at = encrypt_decrypt()._decrypt(AT)
    @property
    def Cookie(self)->Union[Session,login_kuki]:
        session = Session.objects.filter(AccessToken=self.at).first()
        if session:
            return login_kuki(session.cookie_value)
        return session
    
    def isIP(self, ip: list) -> list: 
        return list(filter(lambda x:not matchForSetIP(x), ip))

    def setIPs(self, ip:list)->Union[bool, list]:
        ipl = self.isIP(ip)
        if ipl:
            return ipl
        else:
            user=self.get
            user.allow_ip = json.dumps(ip)
            user.save()
            return True
    
    def setIP(self, ip):
        if matchForSetIP(ip):
            user = self.get.user
            if ip in json.loads(user.allow_ip):
                return False
            user.allow_ip = json.dumps(json.loads(user.allow_ip)+[ip])
            user.save()
            return True
        else:
            return False

    def rmIP(self, ip):
        session = self.get
        ips = json.loads(session.user.allow_ip)
        if ip in ips:
            user=session.user
            ips.remove(ip)
            user.allow_ip = json.dumps(ips)
            user.save()
            return True
        else:
            return False

    @property
    def get(self)->Session:
        user = Session.objects.filter(AccessToken=self.at).first()
        if user:
            return user
        return user

    @property
    def reset_apikey(self)->str:
        session=self.get
        if session:
            user=session.user
            user.apikey = token_urlsafe(32)
            user.save()
            return user.apikey
        else:
            return ""

    @property
    def logOut(self)->bool:
        session=self.get
        if session:
            session.delete()
            return True
        else:
            return False

from requests import Session
from utilities import jsonify
import time
class SimSimi(Session):

    def __init__(self):
        super().__init__()
        self.get("https://simsimi.com/chat") # Get Cookies
        self.url = "https://simsimi.com/api/chats"
        self.lang = "id"

    @property
    def login(self):
        if (info := self.post("https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyClbdTjOMkfilOO2TlyG1THcJ2V0lISbuE", json={"email": "tpjnsgkpgevrg@metalunits.com", "password": "@AnteiCodes12", "returnSecureToken": True}).json()):
            return True if self.post("https://www.simsimi.com/api/accounts/login", json={"timeZone": "Asia/Jakarta", "lc": self.lang, "idToken": info.get("idToken")}).json().get("emailVerify") == True else False
        return False

    @property
    def getCredit(self):
        anu = self.get("https://www.simsimi.com/api/missA?mid=2&pid=10&upid=116424402&checked=%5B%22785246083%22%5D").json()
        return anu if anu.get("reward") else False

    def simi(self, text: str, lang: str="id"):
        """
        :text: String
        :lang: String
        :return: Dict
        """
        self.lang = lang
        if self.login:
            if (tod := self.getCredit):
                param = {"lc": lang, "ft": "1", "normalProb": "1", "reqText": text, "talkCnt": tod.get("cnt")}
                sim = self.get(self.url, params=param).json()
                return {"result": sim.get("respSentence")}
            else:
                return {"result": "Simi gak tau kak"}
        else:
            return {"result": "Simi gak tau kak"}
def sim():
    Simi = SimSimi()
    Simi.login
    credit = Simi.getCredit
    cnt = credit and  credit['cnt']
    ts = time.time()
    while True:
        lang = yield
        text = yield
        if not cnt:
            print(cnt)
            yield {"result":"Simi gak tau kak"}
        elif cnt < 2 or ts - time.time() > 60*8: # login ulang jika Talk Count Habis atau setelah 8 menit
            Simi = SimSimi()
            Simi.login
            credit = Simi.getCredit
            cnt = credit and  credit['cnt']
        ts = time.time()
        yield {"result":Simi.get(Simi.url, params={"lc": lang, "ft": "1", "normalProb": "1", "reqText": text, "talkCnt": cnt}).json()["respSentence"]}
        
simObject = sim()
next(simObject)
def simi(req):
    global simObject
    try:
        if not req.GET.get("text"): return jsonify({"status": 400, "msg": "Parameter text jangan kosong"}, 400)
        lang = req.GET.get("lang","id")
        #s = SimSimi()
        #return jsonify({"status": 200, **s.simi(req.GET.get("text"), lang)}, 200)
        simObject.send(lang)
        resp:dict = simObject.send(req.GET.get("text"))
        next(simObject)
        return jsonify({"status": 200, **resp}, 200)
    except StopIteration:
        simObject = sim()
        next(simObject)
        return jsonify({"status": 200, **{"result":"Simi gak tau kak"}}, 200)

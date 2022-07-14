from emoji import emojize, demojize
from requests import get
from utilities import jsonify
from utilities import send_file

class BaseEmoji:
    BASE_APPLE_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/"
    BASE_GOOGLE_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/298/"
    BASE_SAMSUNG_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/samsung/265/"
    BASE_MICROSOFT_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/microsoft/209/"
    BASE_WHATSAPP_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/whatsapp/273/"
    BASE_TWITTER_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/282/"
    BASE_FACEBOOK_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/facebook/230/"
    BASE_JOYPIXELS_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/joypixels/291/"
    BASE_OPENMOJI_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/openmoji/292/"
    BASE_EMOJIDEX_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/emojidex/112/"
    BASE_MESSENGER_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/facebook/65/"
    BASE_LG_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/lg/57/"
    BASE_MOZILLA_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/mozilla/36/"
    BASE_SOFTBANK_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/softbank/145/"
    BASE_DOCOMO_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/docomo/205/"
    BASE_EMOJIPEDIA_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/emojipedia/294/"

class emojimg(BaseEmoji):
    def __init__(self, emoji="😉", type="whatsapp") -> None:
        self.url = self.BASE_WHATSAPP_URL
        self.emoji = emoji
        if type == "docomo":
            self.url = self.BASE_DOCOMO_URL
        elif type == "softbank":
            self.url = self.BASE_SOFTBANK_URL
        elif type == "mozilla":
            self.url = self.BASE_MOZILLA_URL
        elif type == "lg":
            self.url = self.BASE_LG_URL
        elif type == "messenger":
            self.url = self.BASE_MESSENGER_URL
        elif type == "emojidex":
            self.url = self.BASE_EMOJIDEX_URL
        elif type == "openmoji":
            self.url = self.BASE_OPENMOJI_URL
        elif type == "joypixels":
            self.url = self.BASE_JOYPIXELS_URL
        elif type == "facebook":
            self.url = self.BASE_FACEBOOK_URL
        elif type == "twitter":
            self.url = self.BASE_TWITTER_URL
        elif type == "whatsapp":
            self.url = self.BASE_WHATSAPP_URL
        elif type == "microsoft":
            self.url = self.BASE_MICROSOFT_URL
        elif type == "samsung":
            self.url = self.BASE_SAMSUNG_URL
        elif type == "google":
            self.url = self.BASE_GOOGLE_URL
        elif type == "apple":
            self.url = self.BASE_APPLE_URL
        else:
            pass

    @property
    def emoji2url(self):
        hex_ = '-'.join([format(ord(ch), 'x') for ch in self.emoji])
        name = demojize(self.emoji)[1:-1].lower().replace('_','-')
        url = f"{self.url}{name}_{hex_}.png"
        if get(url).headers.get('content-type') != "image/png":
            return "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/emojipedia/294/hand-with-index-finger-and-thumb-crossed_1faf0.png"
        else:
            return url

def emoji2img(req):
    if (emo := req.GET.get('emoji')):
        emoji = emojimg(emoji=emo)
        if req.GET.get('type'):
            emoji = emojimg(emo, req.GET.get('type'))
        return send_file(emoji.emoji2url)
    else:
        return jsonify({'status': 400, 'msg': 'Parameter emoji jangan kosong'})

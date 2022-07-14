import os
import tempfile
from typing import Union
from simplejson.errors import JSONDecodeError
from .error import FrameNotFound
from .endpoints import (
    TWIBBONE_CLOUD_DRIVE,
    TWIBBONIZE_METADATA,
    TWIBBONE_IMAGE,
    TWIBBONE_SEARCH
)
from io import BytesIO
from PIL import Image
import requests


class SearchTwibonize:
    def __init__(self, query:str='', newer:bool=False, popular:bool=False, support:bool=False) -> None:
        self.sort_by:Union[None, str] = [None, 'recent'][newer] or [None, 'support'][support] or [None, 'popularity'][popular]
        self.json:list = []
        self.query:str = query
        self.page:int  = 0
        self.next_page()
    @property
    def frames(self)->list:
        return [TwibbonizeFrame(frame) for frame in self.json]
    def next_page(self, prev_remove:bool=False, per_page:int=64)->list:
        self.page +=1
        if prev_remove:
            self.json = []
        self.json.extend(requests.get(TWIBBONE_SEARCH, params={**({} if self.sort_by else {'q':self.query}), 'numItems':per_page, 'page':self.page, 'sort':'suitable' if not self.sort_by else self.sort_by}).json())
        return self.frames
    def __str__(self) -> str:
        return f"<[result: {self.json.__len__()} items]>"
    def __repr__(self) -> str:
        return self.__str__()


class Twibbonize:
    def __init__(self, name:str) -> None:
        try:
            self.twibonnize_name:str = name
            self.frame = requests.get(TWIBBONIZE_METADATA+name).json()
            self.name = name
            self.image_twibon = Image.open(BytesIO(requests.get(TWIBBONE_IMAGE+self.frame['frame']).content))
            self.alpha:list = self.findAlpha
        except JSONDecodeError:
            raise FrameNotFound
    def samar(self, image):
        pixel:list = [image.getpixel((0, i)) for i in range(image.height)]+[ image.getpixel((image.width-1, i)) for i in range(image.height) ]
        label:dict = {x: pixel.count(x) for x in set(pixel)}
        maks = {"pixel":(0, 0, 0, 0), "count":0}
        for i in label.keys():
            if maks['count'] < label[i]:
                maks.update({"pixel":i, "count":label[i]})
        return maks['pixel']

    def saveToCloud(self, img): #BytesIO unsuported, i used tempfile instead
        namefile = tempfile.NamedTemporaryFile().name+".jpg"
        img.convert("RGB").save(namefile)
        url=TWIBBONE_CLOUD_DRIVE+requests.post(TWIBBONIZE_METADATA+self.name, data={'campaign_url':self.name}, files={'photo':open(namefile,'rb')}, headers={"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36", "origin": "https://www.twibbonize.com"}).text
        os.remove(namefile)
        return url
    
    @property
    def findAlpha(self):
        kiri:Union[tuple, None]  = None
        atas:Union[tuple, None]  = None
        kanan:Union[tuple, None] = None
        bawah:Union[tuple, None] = None
        for i in range(self.image_twibon.width):
            for x in range(self.image_twibon.height)[:-10]:
                if self.image_twibon.getpixel((i, x))[-1]<255:
                    kiri = (i, x)
                    break
            if kiri:
                break
        for i in range(self.image_twibon.height):
            for x in range(self.image_twibon.width):
                if self.image_twibon.getpixel((x, i))[-1]<255:
                    atas = (x, i)
                    break
            if atas:
                break
        for i in range(self.image_twibon.height)[::-1]:
            for x in range(self.image_twibon.width)[4:]:
                if self.image_twibon.getpixel((x, i))[-1]<255:
                    bawah = (x, i)
                    break
            if bawah:
                break
        for i in range(self.image_twibon.width)[::-1]:
            for x in range(self.image_twibon.height):
                if self.image_twibon.getpixel((i, x))[-1]<255:
                    kanan = ((i, x))
            if kanan:
                break
        return [kiri, kanan, atas, bawah]

    def addToFrame(self, image:Union[str, BytesIO], toLink:bool=False, max_allow_frame=100, quality=100)->Union[BytesIO, str]:
        image_p = Image.open(image)
        bit = BytesIO()
        ukuran_gambar_dbthkan = min(self.alpha[1][0] - self.alpha[0][0], self.alpha[3][1]-self.alpha[2][1])
        if ('is_animated' in dir(image) and image_p.is_animated ) or 'n_frames' in dir(image_p): 
            n = max_allow_frame if image_p.n_frames > max_allow_frame else image_p.n_frames
            frames = []
            duration = image_p.info.get('duration',100)
            samar = self.samar(image_p)
            for i in range(n):
                image_p.seek(i)
                resimage = image_p.resize(self.imageResize(*image_p.size, ukuran_gambar_dbthkan))
                blank = Image.new("RGBA", self.image_twibon.size, samar)
                blank.paste(resimage, (self.alpha[0][0], self.alpha[2][1]), resimage.convert("RGBA"))
                blank.paste(self.image_twibon, (0, 0), self.image_twibon.convert("RGBA"))
                frames.append(blank.convert("RGB"))
            frames[0].save(bit, format='webp', append_images=frames[1:], save_all=True, duration=duration, quality=quality)
            return bit
        else:
            image_p = image_p.convert("RGBA")
            simage = image_p.resize(self.imageResize(*image_p.size,res=ukuran_gambar_dbthkan))
            blank = Image.new("RGBA", self.image_twibon.size, self.samar(simage))
            blank.paste(simage, (self.alpha[0][0], self.alpha[2][1]), simage.convert("RGBA"))
            blank.paste(self.image_twibon, (0, 0), self.image_twibon.convert("RGBA"))
            if toLink:
                return self.saveToCloud(blank)
            blank.convert("RGB").save(bit, format="jpeg")
            return bit


    def imageResize(self, x:int, y:int, res:int=1280)->tuple: #res  = minimal resolution
        if x==y:
            return (res, res)
        elif x<y:
            return (res,int(y/(x/res)))
        elif x>y:
            return  (int(x/(y/res)),res)
        else:
            return (0,0)


class TwibbonizeFrame:
    def __init__(self, js:dict) -> None:
        self.id          = js.get('id', None)
        self.creator:str = js['CampaignCreator']['name']
        self.name:str    = js['name']
        self.url:str     = js['url']
    def useThisFrame(self):
        return Twibbonize(self.url).addToFrame
    def __str__(self) -> str:
        return f"<Frame: {self.name} From: {self.creator}>"
    def __repr__(self) -> str:
        return self.__str__()
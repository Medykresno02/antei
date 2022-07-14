import datetime
import time
reset_apikey = 1
ip_allow = 2
login = 0
class CreateAction:
    def __init__(self) -> None:
        pass
    def reset_apikey(self):
        return [1,time.time()]
    def ip_allow(self, type:str, target:str): # type = 'add' | 'delete'
        assert type in ['add','delete']
        return [2, time.time(), {'add':0, 'delete':1}[type], target]
    def login(self):
        return [0, time.time()]

class Translate:
    taction = lambda self, times:datetime.datetime.fromtimestamp(times).strftime('[%D][%H:%M] ')
    def __init__(self, data) -> None:
        self.data = data
    def translate_reset_apikey(self, data:list):
        return self.taction(data[1])+'Mengatur ulang apikey'
    def translate_ip_allow(self, data:list):
        return self.taction(data[1])+['Menambahkan','Menghapus'][data[2]]+' '+data[3]+[' ke',' dari'][data[2]]+' database'
    def login(self, data:list):
        return self.taction(data[1])
    def __iter__(self):
        for i in self.data:
            yield [self.login, self.translate_reset_apikey, self.translate_ip_allow][i[0]](i)
createAction = CreateAction()
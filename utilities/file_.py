from threading import Event
import sys
from typing import Union
from filetype import (guess_mime as mime, guess_extension as ext)
import signal
import hashlib
import threading
import time
import os
event = Event()

tmpdir = os.path.abspath(os.path.dirname(__file__)+"/../result")
antrian = []

class File:
    def __init__(self) -> None:
        self.filename:str = ''
        self.unique:str = ''
        self.start:float = 0
        self.ext:str = ''
        self.expired:float = 0
        self.size:int = 0
        self.mime:str = ''
        self.binary:bytes = b''


def removeFile(unique):
    global antrian
    for i in antrian:
        if i.unique == unique:
            antrian.remove(i)
            os.remove(f"{tmpdir}/{i.unique}")
            return True
    else:
        return False


def listdir():
    return os.listdir(tmpdir)


def worker():
    global antrian
    while True:
        for i in antrian:
            if i.expired-time.time() < 1:
                print(f"remove: {i.unique}")
                antrian.remove(i)
                os.remove(f"{tmpdir}/{i.unique}")
        if event.is_set():
            break
        time.sleep(1)


def makefile(fn:str, binary:bytes, expired:int=60*60):
    global antrian
    file = File()
    file.size = binary.__len__()
    file.start = time.time()
    file.expired = time.time()+expired
    file.mime = mime(binary)
    file.ext = ext(binary)
    file.filename = fn+"."+file.ext if file.ext else fn
    if not file.mime:
        file.mime = ''
    file.unique = hashlib.blake2s(hashlib.sha256(binary).hexdigest().encode()+file.mime.encode()).hexdigest()
    for i in antrian:
        if i.unique == file.unique:
            return i
    else:
        open(f"{tmpdir}/{file.unique}", "wb").write(binary)
        antrian.append(file)
        return file


def OpenFile(unique:str)->File:
    for i in antrian:
        if unique == i.unique:
            i.binary = open(f"{tmpdir}/{unique}", "rb").read()
            return i
    return File() #False



def stop(x,y):
    global threader
    if x==2:
        event.set()
        if threader._tstate_lock:
            threader._tstate_lock.release_lock()
            threader._stop()
            threader.join()
            if not "test" in sys.argv:
                sys.exit(1)

if "runserver" in sys.argv or "test" in sys.argv:
    threader=threading.Thread(target=worker, args=())
    threader.start()
    signal.signal(2, stop)
    if "test" in sys.argv:
        os.kill(os.getpid(), signal.SIGINT)

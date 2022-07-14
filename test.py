#test auto deploy
import os
import time
import logging
from multiprocessing import Process
from flask import Flask, request
from rich.progress import (
    Progress,
    BarColumn,
)
from threading import Event, Thread
from rich.console import Console
import psutil
import datetime
from ptyprocess import PtyProcessUnicode
konsol = Console()
prog = Progress('[green bold]{task.fields[pidusage]}',BarColumn(bar_width=None), "[green bold]{task.fields[memusage]}[red bold]/[green bold]{task.fields[free]} : [blue bold][progress.percentage]{task.percentage:>3.1f}%")
percentage=0.0
event = Event()
RAM = round(((psutil.virtual_memory().total//1024)//1024)//1024+((psutil.virtual_memory().total//1024)//1024)%1024/1024, 2).__str__()+' GB'
def terpakai():
    s=((psutil.virtual_memory().used//1024)//1024)
    return round((s//1024)+(s%1024)/1024, 2).__str__()+' GB'

def get_pid(pid):
    try:
        mem=int(os.popen("pmap %s|awk -e '/total.*K/{print $2}'|awk -F '[^0-9]*' '$0=$1'"%pid).read())
        return round(mem//1024+(mem%1024)/1024, 3)
    except ValueError:
        return 0
def p_pid(pid):
    jum = get_pid(pid)
    for i in filter(lambda x: x, os.popen(f'pgrep -P {pid}').read().split('\n')):
        jum+=get_pid(i)
    return jum

def kill(sig, c):
    if sig==3:
        event.set()

def stop(prog, sta):
    prog.update(sta, visible=False)
    prog.stop_task(sta)
    prog.stop()

def refresh_prog(prog, sta, pid):
    global percentage
    while True:
        percent=psutil.virtual_memory().percent
        prog.update(sta, memusage=terpakai(), free=RAM, pidusage='[green bold]AnteiAPI [yellow bold]'+round(p_pid(pid)+p_pid(os.getpid()), 2).__str__()+' MB')
        prog.advance(sta, percent-percentage)
        percentage=percent
        if event.is_set():
            stop(prog, sta)
            break
        time.sleep(2)

def spawn(argv:list):
    sta=prog.add_task('Memori',pidusage='[green bold]AnteiAPI [yellow bold]0 MB', total=100, memusage='0MB', free='0MB',start=True)
    prog.start()
    pty = PtyProcessUnicode.spawn(argv)
    Thread(target=refresh_prog, args=(prog,sta,pty.pid)).start()
    while True:
        try:
            pr = pty.read()
            prog.print(pr)
        except KeyboardInterrupt:
            pty.kill(3)
            break
        except Exception:
            break
    event.set()
    stop(prog, sta)
    prog.print('[red bold][[yellow bold]*[red bold]] [blue bold]=> [red bold]Killed')
konsol.print(datetime.datetime.now().strftime('[cyan bikd][%H:%M:%S][green bold] Starting'))
tsk = Process(target=spawn, args=(['python3','manage.py','runserver','0.0.0.0:8080','--insecure'],))
tsk.start()
app = Flask(__name__)
log =logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
@app.route('/', methods=['GET','POST'])
def webhook():
    global tsk
    if request.headers.get('X-Github-Event') in ['push','release']:
        konsol.print(datetime.datetime.now().strftime('[cyan bikd][%H:%M:%S][green bold] Update Available'))
        os.system('git pull https://anteicodesedu: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@github.com/AnteiCodes/Anteiku-API')
        tsk.terminate()
        konsol.print(datetime.datetime.now().strftime('[cyan bold][%H:%M:%S] [green bold]Restarting'))
        tsk = Process(target=spawn, args=(['python3','manage.py','runserver','0.0.0.0:8080','--insecure'],))
        tsk.start()
    return 'oke'

app.run(host='127.0.0.1', port=3000)

from utilities import jsonify
from random import choice
from json import loads

def creep():
    anu = eval(open("result/.creepypasta.json").read())
    return jsonify(choice(anu), 200)

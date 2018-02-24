#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import redirect
from flask import abort
import json
from loco_loader import load_yaml_locos
import controller
from locomotive import locomotive
import time
import sys

c = controller.controller()
load_yaml_locos(c, "locos.yaml")

app = Flask(__name__)

@app.route('/')
def index():
    loco_id = 0
    try:
        loco_id = int(request.args['loco'])
        print('loco: '+str(loco_id))
    except:
        pass
    #{% for action, label in function_list %}
    flist = []
    try:
        flist = c.get_loco(loco_id).get_function_list()
    except:
        pass
    return render_template('index.html', loco_list=c.get_loco_list(), loco_id=loco_id, function_list=flist)

@app.route('/static/<path:path>')
def static_files():
    return send_from_directory('static', path)

@app.route('/emergency', methods=["POST"])
def emergency():
    return ('', 204)

def button_state(loco_id):
    if loco_id == 0:
        return '{"functions":[]}'
    a = dict()
    a["functions"] = []
    for f in c.get_loco(loco_id).get_functions():
        a["functions"].append({ "f_id": str(f.get_id()), "f_state": str(f.get_value())})
    return json.dumps(a)

@app.route('/q', methods=["POST"])
def query():
    loco=int(request.args['loco'])
    if 'action' in request.args.keys():
        if request.args['action'] == 'emergency':
            # TODO: emergency brake here
            return button_state(loco)
        action=int(request.args['action'])
        c.get_loco(loco).toggle_function(action)
    return button_state(loco)

@app.route('/slider', methods=["POST"])
def slider():
    value=int(request.args['value'])
    print("value: "+str(value))
    c.get_loco(47).set_speed(speed=value)
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=False, port=80, host="0.0.0.0")

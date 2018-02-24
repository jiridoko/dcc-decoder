#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import redirect
from flask import abort
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

@app.route('/q', methods=["POST"])
def query():
    loco=int(request.args['loco'])
    if 'action' in request.args.keys():
        action=int(request.args['action'])
        c.get_loco(loco).toggle_function(action)
    return '{ "functions":[{"f_id":"0", "f_state":"on"}, {"f_id":"1", "f_state":"off"}] }'

@app.route('/slider', methods=["POST"])
def slider():
    value=int(request.args['value'])
    print("value: "+str(value))
    c.get_loco(47).set_speed(speed=value)
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=False, port=80, host="0.0.0.0")

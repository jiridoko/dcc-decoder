#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import redirect
from flask import abort
import json
from loco_loader import load_yaml_locos
from point_loader import load_yaml_points
import controller
from locomotive import locomotive
import time
import sys

c = controller.controller()
load_yaml_locos(c, "locos.yaml")
load_yaml_points(c, "points.yaml")

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
    plist = []
    loco_name = "No loco selected"
    loco_serial = "Select one from the menu"
    loco_img = "blank.png"
    max_speed = 14
    try:
        loco = c.get_loco(loco_id)
        flist = loco.get_function_list()
        plist = c.get_point_tuple()
        loco_name = loco.get_nice_name()
        loco_serial = loco.get_serial()
        loco_img = loco.get_img()
        if loco.is_advanced_speed():
            max_speed = 126
    except:
        pass
    return render_template('index.html',\
            loco_list=c.get_loco_list(),\
            loco_id=loco_id,\
            function_list=flist,\
            loco_name=loco_name,\
            loco_serial=loco_serial,\
            loco_img=loco_img,\
            max_speed=max_speed,\
            plist=plist)

@app.route('/static/<path:path>')
def static_files():
    return send_from_directory('static', path)

@app.route('/emergency', methods=["POST"])
def emergency():
    return ('', 204)

def button_state(loco_id):
    if loco_id == 0:
        return '{"functions":[]}'
    loco = c.get_loco(loco_id)
    a = dict()
    a["functions"] = []
    for f in loco.get_functions():
        a["functions"].append({ "f_id": str(f.get_id()), "f_state": str(f.get_value())})
    a["forward"] = str(bool(loco.is_forward()))
    a["speed"] = str(loco.get_speed())
    return json.dumps(a)

@app.route('/cv', methods=["POST"])
def cv():
    loco=int(request.args['loco'])
    cv=int(request.args['cv'])
    value=int(request.args['value'])
    c.get_loco(loco).set_cv(cv=cv, value=value)
    return ('', 204)

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

@app.route('/direction', methods=["POST"])
def direction():
    value=int(request.args['value'])
    loco=int(request.args['loco'])
    c.get_loco(loco).set_direction(forward=(value==1))
    return button_state(loco)

@app.route('/slider', methods=["POST"])
def slider():
    value=int(request.args['value'])
    loco=int(request.args['loco'])
    c.get_loco(loco).set_speed(speed=value)
    return button_state(loco)

if __name__ == '__main__':
    app.run(debug=False, port=80, host="0.0.0.0")

#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import redirect
from flask import abort
import controller
import time
import sys

c = controller.controller()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_2.html')

@app.route('/static/<path:path>')
def static_files():
    return send_from_directory('static', path)

@app.route('/q', methods=["POST"])
def query():
    print("query")
    print("a: "+request.args['a'])
    c.send(controller.controller.loco_functions_1(address=47, f2=True))
    #time.sleep(0.05)
    c.send(controller.controller.loco_functions_1(address=47))
    return ('', 204)

@app.route('/slider', methods=["POST"])
def slider():
    print("value: "+request.args['value'])
    c.send(controller.controller.loco_speed(address=47, speed=int(request.args['value'])))
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=False, port=80, host="0.0.0.0")

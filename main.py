#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import redirect
from flask import abort
import controller
from locomotive import locomotive
import time
import sys

c = controller.controller()
loco1 = locomotive("brejlovec", 47, c)
loco1.add_function("light",         True,  False, 0)
loco1.add_function("sound",         True,  False, 1)
loco1.add_function("horn",          False, False, 2)
loco1.add_function("whistle",       False, False, 3)
loco1.add_function("coupling",      False, False, 4)
loco1.add_function("conductor",     False, False, 5)
loco1.add_function("shunting",      True,  False, 6)
loco1.add_function("curve",         True,  False, 7)
loco1.add_function("sanding",       True,  False, 8)
loco1.add_function("announcement",  False, False, 10)
loco1.add_function("short horn",    False, False, 12)
loco1.add_function("short whistle", False, False, 13)
loco1.add_function("mute",          True,  False, 14)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def static_files():
    return send_from_directory('static', path)

@app.route('/q', methods=["POST"])
def query():
    a=int(request.args['a'])
    print("a: "+str(a))
    loco1.toggle_function(a-1)
    return 'test'

@app.route('/slider', methods=["POST"])
def slider():
    value=int(request.args['value'])
    print("value: "+str(value))
    loco1.set_speed(speed=value)
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=False, port=80, host="0.0.0.0")

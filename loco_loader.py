#!/usr/bin/env python3
import yaml
from locomotive import locomotive

def load_yaml_locos(control, filename):
    with open(filename, 'r') as s:
        struct = yaml.load(s)
        for locos in struct['locomotives']:
            for loco in locos.keys():
                loco_name = str(locos[loco]["name"])
                loco_img = str(locos[loco]["img"])
                loco_serial = str(locos[loco]["serial"])
                loco_id = int(locos[loco]["id"])
                loco_advanced = bool(locos[loco]["advanced_speed"])
                loco_functions = locos[loco]["functions"]
                speed_control = True
                if "speed_control" in locos[loco].keys():
                    speed_control = bool(locos[loco]["speed_control"])
                new_loco = locomotive(str(loco), loco_id, control, advanced_speed=loco_advanced)
                new_loco.set_nice_name(loco_name)
                new_loco.set_serial(loco_serial)
                new_loco.set_img(loco_img)
                new_loco.set_speed_control(speed_control)
                #print(loco_name+" - "+loco_img+" - "+loco_serial+" - "+str(loco_id))
                for function in loco_functions:
                    name = str(function["name"])
                    ident = int(function["id"])
                    default = bool(function["default"])
                    toggle = bool(function["toggle"])
                    label = str(function["label"])
                    fontawesome = bool(function["fa"])
                    new_loco.add_function(name, toggle, default, ident, label, fontawesome)
                    #print(name+" - "+str(ident)+" - "+str(default)+" - "+str(toggle))
                control.add_loco(new_loco)

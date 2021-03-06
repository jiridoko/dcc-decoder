#!/usr/bin/env python3
import dcc
from dcc_signals import *
from urllib import request, parse

class controller(object):
    def __init__(self):
        self.handle = dcc.dcc_init(-1)
        self.locos = dict()
        self.points = []
        self.rail_uri_on_1 = None
        self.rail_uri_on_2 = None
        self.rail_uri_off_1 = None
        self.rail_uri_off_2 = None
        self.rails = False
    def add_rail_uris(self, uri_on_1, uri_on_2, uri_off_1, uri_off_2):
        self.rail_uri_on_1 = uri_on_1
        self.rail_uri_on_2 = uri_on_2
        self.rail_uri_off_1 = uri_off_1
        self.rail_uri_off_2 = uri_off_2
        self.set_rails()
    def switch_rails(self):
        self.rails = not self.rails
        self.set_rails(on=self.rails)
    def get_rails(self):
        return self.rails
    def set_rails(self, on=False):
        url = None
        if on:
            url = [self.rail_uri_on_1, self.rail_uri_on_2]
        else:
            url = [self.rail_uri_off_1, self.rail_uri_off_2]
        if url is not None:
            for one_uri in url:
                print(one_uri)
                req = request.Request(one_uri, data=parse.urlencode({}).encode())
                request.urlopen(req)
    def add_point(self, point):
        self.points.append(point)
    def get_points(self):
        return self.points
    def get_point_tuple(self):
        return [(p.get_name(),\
                p.get_left_url(),\
                p.get_left_img(),\
                p.get_right_url(),\
                p.get_right_img()) for p in self.get_points()]
    def add_loco(self, loco):
        ident = loco.get_id()
        self.locos[ident] = loco
    def get_locos(self):
        return self.locos
    def get_loco(self, ident):
        if ident in self.locos.keys():
            return self.locos[ident]
        else:
            return None
    def get_loco_list(self):
        ret = []
        for i in self.locos.keys():
            loco = self.locos[i]
            ret.append((loco.get_nice_name(), loco.get_id()))
        return ret
    def _format_data(self, data_array):
        arr = data_array
        length = len(arr)
        if length > 5 or length <= 0:
            return None
        if length < 5:
            for i in range(0, 5-length):
                arr.append(0)
        return [length]+arr
    def emergency_stop(self, stop=True):
        data = loco_speed(emergency_stop=stop)
        self.send(data)
        data = loco_speed_advanced(emergency_stop=stop)
        self.send(data)
        for i in self.locos.keys():
            loco = self.locos[i]
            loco.set_speed(speed=0)
    def send(self, data):
        d = self._format_data(data)
        if d is not None:
            ret=dcc.dcc_send(self.handle, d[0], d[1], d[2], d[3], d[4], d[5])
        else:
            raise Exception("Invalid data to be sent")

if __name__ == "__main__":
    from loco_loader import load_yaml_locos
    import time
    c = controller()
    load_yaml_locos(c, "locos.yaml")
    print(str(c.get_loco_list()))
    c.send(loco_set_cv(address=3, cv=1, value=48))
    time.sleep(1)
    c.send(loco_speed_advanced(address=48, speed=37, emergency_stop=False, forward=True))
    time.sleep(5)
    c.send(loco_speed_advanced(address=48, speed=0, emergency_stop=False, forward=True))

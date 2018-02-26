#!/usr/bin/env python3
#import gertbot as gb
import dcc

class controller(object):
    def __init__(self):
        self.handle = dcc.dcc_init(-1)
        self.locos = dict()
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
    def send(self, data):
        d = self._format_data(data)
        if d is not None:
            ret=dcc.dcc_send(self.handle, d[0], d[1], d[2], d[3], d[4], d[5])
        else:
            raise Exception("Invalid data to be sent")

if __name__ == "__main__":
    from loco_loader import load_yaml_locos
    from dcc_signals import *
    import time
    c = controller()
    load_yaml_locos(c, "locos.yaml")
    print(str(c.get_loco_list()))
    c.send(loco_spped_advanced(address=47, speed=56, emergency_stop=False, forward=True))
    time.sleep(5)
    c.send(loco_spped_advanced(address=47, speed=37, emergency_stop=False, forward=True))
    time.sleep(5)
    c.send(loco_spped_advanced(address=47, speed=0, emergency_stop=False, forward=True))

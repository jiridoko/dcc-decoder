#!/usr/bin/env python3
#import gertbot as gb
import dcc
import time

class controller(object):
    def __init__(self):
        self.handle = dcc.dcc_init(-1)
        self.locos = []
    def add_loco(self, loco):
        self.locos.append(loco)
    def get_locos(self):
        return self.locos
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
    c = controller()
    c.send([47, 130])
    c.send([47, 128])

#!/usr/bin/env python3
#import gertbot as gb
import dcc
import time

class controller(object):
    def __init__(self):
        self.handle = dcc.dcc_init(-1)
        print("got handle: "+str(self.handle));
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
            print("self.handle="+str(self.handle))
            ret=dcc.dcc_send(self.handle, d[0], d[1], d[2], d[3], d[4], d[5])
            print("returned: "+str(ret))
        else:
            raise Exception("Invalid data to be sent")

if __name__ == "__main__":
    c = controller()
    print(str(c._format_data([])))
    print(str(c._format_data([1])))
    print(str(c._format_data([1, 2])))
    print(str(c._format_data([1, 2, 3])))
    print(str(c._format_data([1, 2, 3, 4])))
    print(str(c._format_data([1, 2, 3, 4, 5])))
    print(str(c._format_data([1, 2, 3, 4, 5, 6])))
    c.send([47, 130])
    c.send([47, 128])

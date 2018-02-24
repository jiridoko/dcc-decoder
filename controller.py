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
    @staticmethod
    def loco_speed(address=0, speed=0, emergency_stop=False, forward=True, lights=False):
        ret = 0x40 | (forward << 5) | (lights << 4)
        if emergency_stop:
            ret |= 0x01
            return [address, ret]
        if speed == 0:
            return [address, ret]
        elif speed <= 14:
            ret = ret+speed+1
            return [address, ret]
        else:
            return [address, ret]
    @staticmethod
    def loco_functions_1(address=0, lights=False, f1=False, f2=False, f3=False, f4=False):
        ret = 0x80 | (lights << 4) | (f4 << 3) | (f3 << 2) | (f2 << 1) | (f1)
        return [address, ret]
    @staticmethod
    def loco_functions_2(address=0, f5=False, f6=False, f7=False, f8=False):
        ret = 0xB0 | (f8 << 3) | (f7 << 2) | (f6 << 1) | (f5)
        return [address, ret]
    @staticmethod
    def loco_functions_3(address=0, f9=False, f10=False, f11=False, f12=False):
        ret = 0xA0 | (f12 << 3) | (f11 << 2) | (f10 << 1) | (f9)
        return [address, ret]
    @staticmethod
    def loco_functions_4(address=0, f13=False, f14=False, f15=False, f16=False, f17=False, f18=False, f19=False, f20=False):
        ret1 = 0xDE
        ret2 = (f20 << 7) | (f19 << 6) | (f18 << 5) | (f17 << 4) | (f16 << 3) | (f15 << 2) | (f14 << 1) | (f13)
        return [address, ret1, ret2]
    @staticmethod
    def loco_functions_5(address=0, f21=False, f22=False, f23=False, f24=False, f25=False, f26=False, f27=False, f28=False):
        ret1 = 0xDF
        ret2 = (f28 << 7) | (f27 << 6) | (f26 << 5) | (f25 << 4) | (f24 << 3) | (f23 << 2) | (f22 << 1) | (f21)
        return [address, ret1, ret2]

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

#!/usr/bin/env python3

import gertbot as gb
import time
import sys

board = 0

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

def loco_functions_1(address=0, lights=False, f1=False, f2=False, f3=False, f4=False):
    ret = 0x80 | (lights << 4) | (f4 << 3) | (f3 << 2) | (f2 << 1) | (f1)
    return [address, ret]

def loco_functions_2(address=0, f5=False, f6=False, f7=False, f8=False):
    ret = 0xB0 | (f8 << 3) | (f7 << 2) | (f6 << 1) | (f5)
    return [address, ret]

def loco_functions_3(address=0, f9=False, f10=False, f11=False, f12=False):
    ret = 0xA0 | (f12 << 3) | (f11 << 2) | (f10 << 1) | (f9)
    return [address, ret]

def loco_functions_4(address=0, f13=False, f14=False, f15=False, f16=False, f17=False, f18=False, f19=False, f20=False):
    ret1 = 0xDE
    ret2 = (f20 << 7) | (f19 << 6) | (f18 << 5) | (f17 << 4) | (f16 << 3) | (f15 << 2) | (f14 << 1) | (f13)
    return [address, ret1, ret2]

gb.open_uart(0)
#gb.set_mode(board, channel, mode)
gb.set_mode(board, 0, gb.MODE_DCC)

gb.send_dcc_mess(board, 0xF, loco_speed(address=47))
gb.send_dcc_mess(board, 0xF, loco_functions_1(address=47, lights=True, f1=True))
time.sleep(15)
gb.send_dcc_mess(board, 0xF, loco_functions_1(address=47, lights=True, f1=True, f2=True))
gb.send_dcc_mess(board, 0xF, loco_functions_1(address=47, lights=True, f1=True))
time.sleep(5)
for i in range(0,9):
    gb.send_dcc_mess(board, 0xF, loco_speed(address=47, speed=i, lights=True))
    time.sleep(1)
time.sleep(5)
for i in range(0,9):
    gb.send_dcc_mess(board, 0xF, loco_speed(address=47, speed=8-i, lights=True))
    time.sleep(1)
time.sleep(3)
gb.send_dcc_mess(board, 0xF, loco_speed(address=47, speed=7, forward=False, lights=True))
time.sleep(15)
gb.send_dcc_mess(board, 0xF, loco_speed(address=47, speed=0, forward=False, lights=True))
time.sleep(12)
gb.send_dcc_mess(board, 0xF, loco_functions_1(address=47, lights=True))
time.sleep(3)
gb.send_dcc_mess(board, 0xF, loco_functions_1(address=47))

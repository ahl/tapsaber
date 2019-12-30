#!/usr/bin/env python

import board
import digitalio
import time
import getch


white = digitalio.DigitalInOut(board.C1)
black = digitalio.DigitalInOut(board.C0)
black.direction = digitalio.Direction.OUTPUT
black.value = True
white.direction = digitalio.Direction.OUTPUT
white.value = True


def tap(v):
    tnext = time.time()
    value = False
    white.value = value
    value = not value
    for t in v:
        tnext += t / 1000
        while time.time() < tnext:
            pass
        white.value = value
        value = not value


def left():
    tap([17.7 + 15.7, 2, 2, 2, 4, 2, 2, 2, 2])


def right():
    tap([17.7 + 15.7, 2, 2, 2, 4, 2, 2, 2, 4])


while True:
    c = getch.getch()
    if c == 'j':
        left()
    elif c == 'k':
        right()
    elif c == 'c':
        break

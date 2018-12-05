try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    from tkinter import *

import pygame as pyg

import random
import time

print("Test")

# Test code for pygame
pyg.init()
screen = pyg.display.set_mode((128, 128))
clock = pyg.time.Clock()

counter, text = 10, '10'.rjust(3)
pyg.time.set_timer(pyg.USEREVENT, 1000)
font = pyg.font.SysFont('Consolas', 30)

while True:
    for e in pyg.event.get():
        if e.type == pyg.USEREVENT:
            counter -= 1
            text = str(counter).rjust(3) if counter > 0 else 'boom!'
        if e.type == pyg.QUIT: break
    else:
        screen.fill((255, 255, 255))
        screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
        pyg.display.flip()
        clock.tick(60)
        continue
    break

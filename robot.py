# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:38:23 2018

@author: swaprava
"""

#import time
#import curses
#
#def pbar(window):
#    for i in range(10):
#        window.addstr(10, 10, "[" + ("=" * i) + ">" + (" " * (10 - i )) + "]")
#        window.refresh()
#        time.sleep(0.5)
#
#curses.wrapper(pbar)

#import sys
#import time
#
#for i in range(10):
#    sys.stdout.write("\r{0}>".format("="*i))
#    sys.stdout.flush()
#    time.sleep(0.5)
  
from tkinter import *
import time

window = Tk()

window.title("Decentralized Robot Collision Avoidance")

canvas = Canvas(window, width=800, height=600)
canvas.pack()
x1 = canvas.create_rectangle(100,100,110,110, fill='blue')
x2 = canvas.create_rectangle(200,200,210,210, fill='red')

obstacle = canvas.create_rectangle(110,110,150,150, fill='orange')

for i in range(10):
    
    if i < 5:
        canvas.move(x1, 10, 0)
    else:
        canvas.move(x1, 0, 10)
    canvas.move(x2, -10, 0)
#    canvas.r
    window.update()
    time.sleep(1)
    
window.mainloop()

#from Tkinter import *
#import math
#
#WIDTH = 400
#HEIGHT = 400
#CANVAS_MID_X = WIDTH/2
#CANVAS_MID_Y = HEIGHT/2
#SIDE = WIDTH/4
#
#root = Tk()
#canvas = Canvas(root, bg="black", height=HEIGHT, width=WIDTH)
#canvas.pack()
#
#vertices = [
#    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y - SIDE/2],
#    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y - SIDE/2],
#    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y + SIDE/2],
#    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y + SIDE/2],
#]
#
#def rotate(points, angle, center):
#    angle = math.radians(angle)
#    cos_val = math.cos(angle)
#    sin_val = math.sin(angle)
#    cx, cy = center
#    new_points = []
#    for x_old, y_old in points:
#        x_old -= cx
#        y_old -= cy
#        x_new = x_old * cos_val - y_old * sin_val
#        y_new = x_old * sin_val + y_old * cos_val
#        new_points.append([x_new + cx, y_new + cy])
#    return new_points
#
#def draw_square(points, color="red"):
#    canvas.create_polygon(points, fill=color)
#
#def test():
#    old_vertices = [[150, 150], [250, 150], [250, 250], [150, 250]]
#    print "vertices: ", vertices, "should be: ", old_vertices
#    print vertices == old_vertices
#
#draw_square(vertices, "blue")
#
#center = (CANVAS_MID_X, CANVAS_MID_Y)
#new_square = rotate(vertices, 30, center)
#test()
#draw_square(new_square)
#
#mainloop()

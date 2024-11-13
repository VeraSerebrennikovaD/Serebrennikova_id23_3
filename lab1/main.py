#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from math import sin, cos, pi

root = Tk()
angle = 0
canvas = Canvas(root, width = 600, height = 600)
canvas.pack()
canvas.create_oval(300 - 200, 300 - 200, 300 + 200, 300 + 200, outline = 'black')
point = canvas.create_oval(0, 0, 5, 5, fill = 'black')
r = 200
direction = 1 # Для определения направления движения
speed = 0.01 # Для определения скорости движения
angle = 0

def animation():
    global angle
    x = 300 + sin(angle) * r
    y = 300 + cos(angle) * r
    canvas.coords(point, x - 10, y - 10, x + 10, y + 10)
    angle += direction * speed
    if angle > pi * 2:
        angle -= pi * 2
    if angle < 0:
        angle += pi * 2
    canvas.after(10, animation)
    
animation()
        
root.mainloop()


# ![image.png](attachment:image.png)

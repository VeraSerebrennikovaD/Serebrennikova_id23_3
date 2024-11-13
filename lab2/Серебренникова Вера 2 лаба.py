#!/usr/bin/env python
# coding: utf-8

# In[6]:


import tkinter as tk
import random
import math
import json

PASTEL_COLORS = [
    "#FFB3BA",  # красный
    "#FFDFBA",  # оранжевый
    "#FFFFBA",  # жёлтый
    "#BAFFC9",  # зелёный
    "#BAE1FF",  # голубой
    "#E3BAFF",  # фиолетовый
    "#FFC2E3"  # розовый
]

with open('config.json', 'r') as file:
    config = json.load(file)

root = tk.Tk()
root.title("Окно, в котором дождь капает")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Список капель — здесь будут храниться все текущие капли дождя
drops = []

# Функция для создания капли дождя
def create_raindrop(canvas):
    x = random.randint(0, canvas.winfo_width())
    y = random.randint(0, canvas.winfo_height())
    length = random.randint(5, 30)
    speed = random.uniform(config['min_speed'], config['max_speed'])
    angle = random.uniform(config['min_angle'], config['max_angle'])
    width = random.randint(1, config['max_width'])
    color = random.choice(PASTEL_COLORS)
    raindrop_id = canvas.create_line(
        x, y,
        x + length * math.sin(math.radians(angle)),
        y + length * math.cos(math.radians(angle)),
        fill=color, width=width
        )

    return {'id': raindrop_id, 'x': x, 'y': y, 'length': length, 'speed': speed, 'angle': angle, 'width': width}


# Функция для создания всех капель в начале симуляции
def generate_raindrops():
    for _ in range(config['density']): # 'density' - плотность. Сколько плотность, столько и капель
        drop = create_raindrop(canvas)
        drops.append(drop)


# Функция для перемещения капли дождя на холсте
def move_raindrop(canvas, drop):
    dx = drop['speed'] * math.sin(math.radians(drop['angle']))
    dy = drop['speed'] * math.cos(math.radians(drop['angle']))
    canvas.move(drop['id'], dx, dy)
    # Обновляем текущие координаты капли в её словаре
    drop['x'] += dx
    drop['y'] += dy
    # Если капля выходит за нижнюю границу холста, перемещаем её наверх (создаём эффект "бесконечного дождя")
    if drop['y'] > canvas.winfo_height():
        drop['y'] -= drop['length'] + canvas.winfo_height()
        drop['x'] = random.randint(0, canvas.winfo_width())
        canvas.coords( # coords() устанавливает новые координаты для линии
            drop['id'], drop['x'], drop['y'],
            drop['x'] + drop['length'] * math.sin(math.radians(drop['angle'])),
            drop['y'] + drop['length'] * math.cos(math.radians(drop['angle']))
        )
        
# Функция для обновления положения всех капель
def update_drops():
    for drop in drops:
        move_raindrop(canvas, drop)
    # Обновление каждые 50 миллисекунд
    root.after(50, update_drops)


# Ожидаем полной инициализации холста, чтобы избежать ошибок при добавлении капель
root.after(100, generate_raindrops)
# иначе они пойдут все из одной точки, так как окно Tkinter разворачивается по окружности, и в самом начале будет загружен лишь 1 пиксель
root.after(150, update_drops)  # Начинаем перемещать капли через 150 миллисекунд

root.mainloop()


#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pyqt5')
get_ipython().system('pip install pyqt5-tools')


# In[ ]:


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QPushButton, QLineEdit, \
    QSpinBox, QSlider, QDialog, QLabel
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QPoint
import sys
import random
import math
import json
import os

CONFIG_FILE = 'config.json'


def load_config():
    # Устанавливаем базовые значения по умолчанию
    default_config = {
        "drop_frequency": 1,
        "drop_speed": 3,
        "drop_length": 10
    }

    # Проверяем, существует ли файл config.json
    if os.path.exists(CONFIG_FILE):
        # Если файл существует, пробуем загрузить его
        with open(CONFIG_FILE, 'r') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = default_config  # Если ошибка в файле, применяем значения по умолчанию
    else:
        # Если файл не существует, создаем его с значениями по умолчанию
        config = default_config
        save_config(config)

    return config


def save_config(config):
    # Сохраняем конфигурацию в файл config.json
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


class Raindrop:
    # Класс "Капля" описывает поведение капли дождя
    def __init__(self, position, angle, speed, length):
        self.position = position
        self.angle = angle
        self.length = length
        self.speed = speed

    def move(self):
        # Перемещаем каплю согласно её углу и скорости
        self.position[0] += math.cos(self.angle) * self.speed
        self.position[1] += math.sin(self.angle) * self.speed


class Cloud:
    # Класс "Облако" описывает поведение облака и генерацию капель
    def __init__(self, position, shape='ellipse', config=None):
        if config is None:
            config = load_config()

        self.position = position
        self.raindrops = []
        self.drop_frequency = config.get("drop_frequency", 1)  # Загружаем частоту капель из конфигурации
        self.drop_speed = config.get("drop_speed", 3)  # Скорость капель
        self.drop_length = config.get("drop_length", 10)  # Длина капель
        self.shape = shape  # Форма облака ('ellipse' или 'rectangle')

    def generate_raindrop_position(self):
        # Генерация начальной позиции капли в зависимости от формы облака
        if self.shape == 'rectangle':
            # Для прямоугольника - от любой точки нижнего края
            x_position = self.position[0] + random.uniform(0, 50)
            y_position = self.position[1] + 30
        else:
            # Для эллипса - от нижней половины периметра эллипса
            angle = random.uniform(math.pi / 4, 3 * math.pi / 4)
            x_position = self.position[0] + 25 + 25 * math.cos(angle)
            y_position = self.position[1] + 15 + 15 * math.sin(angle)

        return [x_position, y_position]

    def update_raindrops(self):
        # Создание капли в зависимости от частоты
        if random.random() < self.drop_frequency * 0.1:
            drop_position = self.generate_raindrop_position()
            angle = math.radians(90) + random.uniform(-math.radians(15), math.radians(15))
            drop = Raindrop(drop_position, angle, self.drop_speed, self.drop_length)
            self.raindrops.append(drop)

        # Удаление капель, вышедших за пределы окна
        self.raindrops = [drop for drop in self.raindrops if drop.position[1] <= 600]


class CloudSettingsDialog(QDialog):
    # Диалоговое окно для настройки параметров облака
    def __init__(self, cloud, parent=None):
        super().__init__(parent)
        self.cloud = cloud
        self.setWindowTitle("Настройка этого прекрасного облачка")
        
        # Создаем крутилки для настройки частоты, скорости и длины капель
        self.drop_frequency_slider = QSlider(Qt.Horizontal)
        self.drop_frequency_slider.setRange(1, 10)
        self.drop_frequency_slider.setValue(self.cloud.drop_frequency)

        self.drop_speed_slider = QSlider(Qt.Horizontal)
        self.drop_speed_slider.setRange(1, 10)
        self.drop_speed_slider.setValue(self.cloud.drop_speed)

        self.drop_length_slider = QSlider(Qt.Horizontal)
        self.drop_length_slider.setRange(5, 50)
        self.drop_length_slider.setValue(self.cloud.drop_length)

        # Настройка расположения элементов
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Частота капель"))
        layout.addWidget(self.drop_frequency_slider)
        layout.addWidget(QLabel("Скорость капель"))
        layout.addWidget(self.drop_speed_slider)
        layout.addWidget(QLabel("Длина капель"))
        layout.addWidget(self.drop_length_slider)

        # Кнопка ОК
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def accept(self):
        # Применяем изменения к облаку
        self.cloud.drop_frequency = self.drop_frequency_slider.value()
        self.cloud.drop_speed = self.drop_speed_slider.value()
        self.cloud.drop_length = self.drop_length_slider.value()
        super().accept()


class MainWindow(QWidget):
    # Основное окно симуляции дождя
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Дождик кап-кап")
        self.setGeometry(100, 100, 800, 600)
        self.config = load_config()

        # Кнопки управления
        self.start_button = QPushButton("Старт")
        self.stop_button = QPushButton("Стоп")
        self.add_cloud_button = QPushButton("+ облачко")
        self.remove_cloud_button = QPushButton("- облачко")

        # Задаем размер кнопок
        for button in [self.start_button, self.stop_button, self.add_cloud_button, self.remove_cloud_button]:
            button.setFixedSize(80, 30)

        # Размещение кнопок
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.add_cloud_button)
        button_layout.addWidget(self.remove_cloud_button)
        button_layout.addStretch(1)

        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        # Переменные и таймеры для облаков
        self.clouds = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)

        self.drop_timer = QTimer(self)
        self.drop_timer.timeout.connect(self.update_raindrops)

        # Подключаем действия к кнопкам
        self.start_button.clicked.connect(self.start_simulation)
        self.stop_button.clicked.connect(self.stop_simulation)
        self.add_cloud_button.clicked.connect(self.add_cloud)
        self.remove_cloud_button.clicked.connect(self.remove_cloud)

        # Устанавливаем параметры для обновления дождя
        self.drop_update_interval = 200
        self.simulation_active = False
        self.drop_timer.start(self.drop_update_interval)

    def start_simulation(self):
        # Запуск симуляции
        self.simulation_active = True
        self.timer.start(50)
        self.drop_timer.start(self.drop_update_interval)

    def stop_simulation(self):
        # Остановка симуляции
        self.simulation_active = False
        self.timer.stop()
        self.drop_timer.stop()

    def add_cloud(self, shape='ellipse'):
        # Добавляем облако с параметрами из config.json
        new_cloud_position = [random.randint(50, 700), random.randint(50, 200)]
        shape = random.choice(['ellipse', 'rectangle'])  # Случайная форма
        self.clouds.append(Cloud(new_cloud_position, shape, self.config))
        self.update()

    def remove_cloud(self):
        # Удаление последнего облака
        if self.clouds:
            self.clouds.pop()
            self.update()  # Перерисовка экрана после удаления облака

    def update_simulation(self):
        # Обновляем все облака и капли
        for cloud in self.clouds:
            cloud.update_raindrops()
            for drop in cloud.raindrops:
                drop.move()
        self.update()

    def paintEvent(self, event):
        # Метод отрисовки облаков и капель
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for cloud in self.clouds:
            painter.setPen(QPen(QColor(128, 128, 128), 2))
            painter.setBrush(QColor(200, 200, 200))
            if cloud.shape == 'rectangle':
                painter.drawRect(int(cloud.position[0]), int(cloud.position[1]), 50, 30)
            else:
                painter.drawEllipse(int(cloud.position[0]), int(cloud.position[1]), 50, 30)

            for drop in cloud.raindrops:
                pastel_color = QColor(random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
                painter.setPen(QPen(pastel_color, 2))
                end_x = drop.position[0] + math.cos(drop.angle) * drop.length
                end_y = drop.position[1] + math.sin(drop.angle) * drop.length
                painter.drawLine(int(drop.position[0]), int(drop.position[1]), int(end_x), int(end_y))

    # Управление событиями мыши для перемещения и настройки облаков
    def mousePressEvent(self, event):
        for cloud in self.clouds:
            if self.is_inside_cloud(event.pos(), cloud):
                self.selected_cloud = cloud
                self.cloud_dragging = True # режим перетаскивания
                self.drag_offset = (event.pos().x() - cloud.position[0], event.pos().y() - cloud.position[1]) # смещение для перетаскивания, чтобы сохранить относительную позицию клика в пределах облака
                break

    def mouseMoveEvent(self, event):
        if self.cloud_dragging and self.selected_cloud:
            self.selected_cloud.position[0] = event.pos().x() - self.drag_offset[0]
            self.selected_cloud.position[1] = event.pos().y() - self.drag_offset[1]
            self.update()

    def mouseReleaseEvent(self, event):
        self.cloud_dragging = False

    def is_inside_cloud(self, point, cloud):
        # Проверяем, находится ли точка внутри эллипса (облака)
        ellipse_center = QPoint(cloud.position[0], cloud.position[1])
        ellipse_radius_x = 50
        ellipse_radius_y = 30

        dx = point.x() - ellipse_center.x()
        dy = point.y() - ellipse_center.y()

        return (dx ** 2) / (ellipse_radius_x ** 2) + (dy ** 2) / (ellipse_radius_y ** 2) <= 1

    def mouseDoubleClickEvent(self, event):
        for cloud in self.clouds:
            if self.is_inside_cloud(event.pos(), cloud):
                dialog = CloudSettingsDialog(cloud, self)
                if dialog.exec_() == QDialog.Accepted: # ждем реакции пользователя
                    break

    def update_raindrops(self):
        if self.simulation_active:
            for cloud in self.clouds:
                cloud.update_raindrops()
                for drop in cloud.raindrops:
                    if drop.position[1] > self.height():
                        cloud.raindrops.remove(drop)
            self.update()


app = QApplication(sys.argv) # Приложение
window = MainWindow()
window.show()
sys.exit(app.exec_()) # пока приложение не будет закрыто


# In[ ]:





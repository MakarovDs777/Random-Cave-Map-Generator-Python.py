import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

def generate_fractal_field(shape, min_length, angle, scale):
    array = np.zeros(shape, dtype=float)
    center = np.array(shape) // 2
    length = min(shape) // 2
    draw_fractal(center, length, min_length, angle, array, scale)
    return array

def draw_fractal(start, length, min_length, angle, array, scale):
    if length > min_length:
        end = start + length * np.array([np.cos(angle), np.sin(angle), np.sin(angle)])
        num_points = int(length * scale)
        for i in range(num_points):
            t = i / num_points
            point = start + t * (end - start)
            point = np.round(point).astype(int)
            if np.all(point >= 0) and np.all(point < np.array(array.shape)):
                array[tuple(point)] = 1
        
        # Рекурсивный вызов для левой и правой ветвей
        draw_fractal(end, length * 0.75, min_length, angle - np.pi / 4, array, scale)
        draw_fractal(end, length * 0.75, min_length, angle + np.pi / 1, array, scale)

def save_obj(vertices, edges, filename):
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for edge in edges:
            f.write(f"l {edge[0]+1} {edge[1]+1}\n")  # OBJ индексы начинаются с 1

def on_key(event, vertices, edges):
    if event.key == 'r':
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "fractal.obj")
        save_obj(vertices, edges, desktop_path)
        print(f"OBJ файл сохранен на рабочем столе как 'fractal.obj'")

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива
scale = 2  # Масштабирование координат для массива
min_length = 2
angle = np.pi / 2

# Генерация 3D-поля
fractal_field = generate_fractal_field(shape, min_length, angle, scale)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(fractal_field, level=0.5)

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
fig.canvas.mpl_connect('key_press_event', lambda event: on_key(event, verts, faces))
plt.show()

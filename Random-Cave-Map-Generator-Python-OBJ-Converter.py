import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
import os
import random 

def draw_fractal_tree(x, y, z, length, min_length, angle_xy, angle_z, array, scale):
    if length > min_length:
        # Рассчитываем координаты следующей точки
        new_x = x + length * np.cos(angle_xy) * np.cos(angle_z)
        new_y = y + length * np.sin(angle_xy) * np.cos(angle_z)
        new_z = z + length * np.sin(angle_z)

        # Заполняем массив значением 1 в текущей точке и всех точках на пути к следующей точке
        num_points = int(length * scale)
        for i in range(num_points):
            t = i / num_points
            point = np.round(np.array([x, y, z]) + t * (np.array([new_x, new_y, new_z]) - np.array([x, y, z]))).astype(int)
            if np.all(point >= 0) and np.all(point < np.array(array.shape)):
                array[tuple(point)] = 1

        # Рекурсивный вызов для левой и правой ветвей
        draw_fractal_tree(new_x, new_y, new_z, length * 0.75, min_length, angle_xy - np.pi / 4, angle_z + np.pi / 8, array, scale)
        draw_fractal_tree(new_x, new_y, new_z, length * 0.75, min_length, angle_xy + np.pi / random.randint(1, 2), angle_z - np.pi / 8, array, scale)

def save_fractal(verts, faces, filename):
    try:
        with open(filename, 'w') as f:
            for v in verts:
                f.write('v {:.6f} {:.6f} {:.6f}\n'.format(v[0], v[1], v[2]))
            for face in faces:
                f.write('f {} {} {}\n'.format(face[0]+1, face[1]+1, face[2]+1))
        print(f"Model saved as {filename}")
    except Exception as e:
        print(f"Error saving model: {e}")

# Начальные параметры
x, y, z = 0, 0, 0
length = 100
min_length = 5
angle_xy = np.pi / 2  # Угол в плоскости XY
angle_z = 0           # Начальный угол по оси Z
scale = 2  # Масштабирование координат для массива

# Создаем 3D массив и вызываем функцию для рисования фрактала
shape = (100, 100, 100)
array = np.zeros(shape, dtype=float)
draw_fractal_tree(x, y, z, length, min_length, angle_xy, angle_z, array, scale)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(array, level=0.5)

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Визуализация модели
verts = verts * np.array(shape)
verts -= np.min(verts, axis=0)  # Центрируем модель
verts /= np.max(verts)          # Нормализуем модель

# Создаем коллекцию полигонов для визуализации
poly3d = Poly3DCollection(verts[faces], alpha=0.5, edgecolor='k')
ax.add_collection3d(poly3d)

# Настройки отображения
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.auto_scale_xyz([0, 1], [0, 1], [0, 1])  # Устанавливаем диапазоны для осей

# Показываем окно с моделью
plt.show()

# Сохранение фрактала в формате OBJ
output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'fractal.obj')
save_fractal(verts, faces, output_path)

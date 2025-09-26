import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time
from scipy.spatial import ConvexHull


def load_points(filename):
    """
    Читает файл с координатами точек.
    Формат каждой строки: x, y
    Возвращает np.array формы (N, 2)
    """
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # пропускаем пустые строки
            x_str, y_str = line.split(',')
            x = float(x_str.strip())
            y = float(y_str.strip())
            points.append([x, y])
    return np.array(points)

def parse_hulls(filename: str):
    hulls = []
    current_hull = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # пропускаем пустые строки

            if line.startswith("Hull"):
                if current_hull:
                    hulls.append(np.array(current_hull, dtype=float))
                    current_hull = []
            else:
                x, y = map(float, line.split(","))
                current_hull.append([x, y])

        # не забываем добавить последний hull
        if current_hull:
            hulls.append(np.array(current_hull, dtype=float))

    return hulls

def onion_layers(points):
    """
    points: np.array с формой (N,2)
    возвращает список слоев (каждый слой — np.array)
    """
    layers = []
    pts = points.copy()

    while len(pts) >= 3:
        hull = ConvexHull(pts)
        layer = pts[hull.vertices]
        layers.append(layer)

        # удалить точки, которые входят в текущий слой
        mask = np.ones(len(pts), dtype=bool)
        mask[hull.vertices] = False
        pts = pts[mask]

    return layers


def hulls_equal(hulls_cpp, hulls_py, tol=1e-8):
    """
    hulls_cpp, hulls_py: списки слоев, каждый слой — np.array формы (N,2)
    tol: допустимая погрешность для координат
    """
    if len(hulls_cpp) != len(hulls_py):
        return False

    for layer_cpp, layer_py in zip(hulls_cpp, hulls_py):
        if len(layer_cpp) != len(layer_py):
            return False
        
        # проверяем, что все точки совпадают как множества
        set_cpp = set(map(tuple, np.round(layer_cpp/tol).astype(int)))
        set_py = set(map(tuple, np.round(layer_py/tol).astype(int)))

        if set_cpp != set_py:
            return False

    return True


hulls_cpp = parse_hulls("output_hulls.txt")

points = load_points("points.txt")

hulls_py = onion_layers(points)

cpp = sorted(hulls_cpp, key=len)
pyt = sorted([len(x) for x in hulls_py])

print(len(cpp[0]))
print(pyt)

print(hulls_equal(hulls_cpp, hulls_py))

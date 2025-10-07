import numpy as np
from scipy.spatial import ConvexHull


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
import numpy as np


def load_points(filename):
    """
    Читает файл с координатами точек.
    Первая строка: количество точек
    Последующие строки: x y (разделены пробелами)
    Возвращает np.array формы (N, 2)
    """
    with open(filename, 'r') as f:
        # Пропускаем первую строку и читаем все остальные
        return np.array([list(map(float, line.split())) 
                        for line in f.readlines()[1:] 
                        if line.strip()])
    

def parse_func_depth(fname):
    data = np.loadtxt(fname)
    return data


def parse_hulls(filename: str):
    hulls = []
    current_hull = []
    execution_time = None

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # пропускаем пустые строки

            # Парсим время выполнения
            if line.startswith("Execution time:") and execution_time is None:
                time_str = line.split(": ")[1]  # "0.034252 seconds"
                time_value = float(time_str.split()[0])  # 0.034252
                execution_time = time_value
                continue

            if line.startswith("Hull"):
                if current_hull:
                    hulls.append(np.array(current_hull, dtype=float))
                    current_hull = []
            else:
                # Пропускаем строки, которые не являются координатами
                if "," in line:
                    x, y = map(float, line.split(","))
                    current_hull.append([x, y])

        # не забываем добавить последний hull
        if current_hull:
            hulls.append(np.array(current_hull, dtype=float))

    return hulls, execution_time

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time


def write_to_file(points, filename):
    with open(filename, "w") as f:
        for x, y in points:
            f.write(f"{x}, {y}\n")


def read_from_file(filename):
    points = []
    with open(filename, "r") as f:
        for line in f:
            x_str, y_str = line.strip().split(",")
            points.append([float(x_str), float(y_str)])
    return np.array(points)


def plot_hull(points, hull):
    plt.scatter(points[:, 0], points[:, 1], color='blue')
    plt.plot(hull[:, 0], hull[:, 1], 'r-', label=f"Convex Hull ({len(hull)-1})")
    plt.scatter(hull[:, 0], hull[:, 1], color='red')
    plt.title("Convex Hull for a set of points")
    plt.grid(True)
    plt.legend()
    plt.show()


points = np.random.standard_normal((1000, 2))
print("Points was generated -> Write to file")
write_to_file(points, "points.txt")
print("Points were written into file -> Find convex hull")
start = time.time()
subprocess.run(["./main"])
print(f'Time = {time.time() - start}')
print("Convex hull was found -> Read hull")
hull = read_from_file("output_points.txt")
print("Hull was saved -> Plot the hull")
plot_hull(points, hull)

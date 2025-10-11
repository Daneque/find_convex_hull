import subprocess
from FileUtilsPy import parse_hulls, parse_func_depth


def call_cpp(input_fname, func_depth, algo="Graham",
             output_fname="output_hulls.txt", points_depth="points_depth.txt"):
    subprocess.run(["main.exe",
                    input_fname,
                    algo, func_depth,
                    output_fname,
                    points_depth])
    hulls, exec_time = parse_hulls(output_fname)
    func_depth_data = parse_func_depth(func_depth)
    return hulls, exec_time, func_depth_data

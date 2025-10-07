import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time
from scipy.spatial import ConvexHull
from plot_scripts import plot_onion_decomposition
from FileUtilsPy import load_points, parse_hulls, parse_func_depth
from HullsTools import onion_layers, hulls_equal
import os
import pandas as pd



def call_cpp(input_fname, func_depth, algo="Graham", output_fname="output_hulls.txt", points_depth="points_depth.txt"):

    subprocess.run(["main.exe", input_fname, algo, func_depth, output_fname, points_depth])

    hulls, exec_time = parse_hulls(output_fname)

    func_depth_data = parse_func_depth(func_depth)

    return hulls, exec_time, func_depth_data


def execute_fish_and_bird():
    fnames = os.listdir("Fish_and_bird")
    
    # Создаем список для хранения данных
    data = []
    
    for input_fname in fnames:
        clear_name = input_fname.split('.')[0]
        
        input_fname = "Fish_and_bird/" + input_fname
        func_depth = "Fish_and_bird_exps/" + "func_depth_" + clear_name + ".txt"
        output_fname = "Fish_and_bird_exps/" + "output_" + clear_name + ".txt"
        points_depth = "Fish_and_bird_exps/" + "points_depth_" + clear_name + ".txt"
        
        # Запускаем Jarvis
        hulls, exec_time_jarvis, func_depth_data = call_cpp(
            input_fname=input_fname, 
            func_depth=func_depth, 
            algo="Jarvis", 
            output_fname=output_fname, 
            points_depth=points_depth
        )
        
        # Запускаем Graham
        _, exec_time_graham, _ = call_cpp(
            input_fname=input_fname, 
            func_depth=func_depth, 
            algo="Graham", 
            output_fname=output_fname, 
            points_depth=points_depth
        )
        
        M = len(hulls)
        
        # Добавляем данные в список
        data.append({
            'filename': clear_name,
            'N points': func_depth_data[:, 1].sum(),
            'M_layers': M,
            'time_Jarvis_ms': exec_time_jarvis,
            'time_Graham_ms': exec_time_graham,
            'time_ratio': exec_time_jarvis / exec_time_graham if exec_time_graham != 0 else float('inf')
        })
    
    # Создаем DataFrame
    df = pd.DataFrame(data)
    
    # Сортируем по имени файла (опционально)
    df = df.sort_values('filename')
    
    # Сохраняем в разные форматы
    # df.to_csv('algorithm_comparison.csv', index=False)
    df.to_excel('algorithm_comparison.xlsx', index=False)
    
    # Выводим статистику
    print("\n" + "="*50)
    print("СТАТИСТИКА АЛГОРИТМОВ:")
    print("="*50)
    print(f"Всего файлов: {len(df)}")
    print(f"Среднее время Jarvis: {df['time_Jarvis_ms'].mean():.10f} ms")
    print(f"Среднее время Graham: {df['time_Graham_ms'].mean():.10f} ms")
    print(f"Медианное отношение времени (Jarvis/Graham): {df['time_ratio'].median():.2f}")
    
    # Подсчитываем, какой алгоритм быстрее в каждом случае
    faster_jarsiv = (df['time_Jarvis_ms'] < df['time_Graham_ms']).sum()
    faster_graham = (df['time_Graham_ms'] < df['time_Jarvis_ms']).sum()
    print(f"Jarvis быстрее в: {faster_jarsiv} случаях")
    print(f"Graham быстрее в: {faster_graham} случаях")

    print("\n" + "="*50)
    print("ТОП-5 самых долгих случаев для Jarvis:")
    print(df.nlargest(5, 'time_Jarvis_ms')[['filename', 'time_Jarvis_ms', 'time_Graham_ms']])

    print("\nТОП-5 самых долгих случаев для Graham:")
    print(df.nlargest(5, 'time_Graham_ms')[['filename', 'time_Jarvis_ms', 'time_Graham_ms']])
    
    return df

# Запускаем функцию
results_df = execute_fish_and_bird()

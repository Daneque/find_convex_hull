import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import FileUtilsPy as fup
from script import call_cpp


class ConvexHullGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull Visualization")
        self.root.geometry("1200x900")
        
        # Переменные
        self.selected_file = tk.StringVar()
        self.directory_var = tk.StringVar(value="Files")  # Начальная директория
        self.save_directory_var = tk.StringVar(value="Results")  # Директория для сохранения
        self.algorithm_var = tk.StringVar(value="Jarvis")
        self.max_layers_var = tk.StringVar(value="10")
        self.plot_depth_var = tk.BooleanVar(value=False)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель - элементы управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 1. Ввод директории с данными
        dir_frame = ttk.LabelFrame(control_frame, text="Data Directory")
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(dir_frame, text="Input Directory:").pack(anchor=tk.W)
        
        dir_input_frame = ttk.Frame(dir_frame)
        dir_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.dir_entry = ttk.Entry(dir_input_frame, textvariable=self.directory_var)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(dir_input_frame, text="Browse", 
                  command=self.browse_input_directory).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(dir_frame, text="Refresh Files", 
                  command=self.load_files).pack(fill=tk.X, pady=(5, 0))
        
        # 2. Директория для сохранения
        save_dir_frame = ttk.LabelFrame(control_frame, text="Save Directory")
        save_dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(save_dir_frame, text="Output Directory:").pack(anchor=tk.W)
        
        save_dir_input_frame = ttk.Frame(save_dir_frame)
        save_dir_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.save_dir_entry = ttk.Entry(save_dir_input_frame, textvariable=self.save_directory_var)
        self.save_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(save_dir_input_frame, text="Browse", 
                  command=self.browse_save_directory).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(save_dir_frame, text="Create Directory", 
                  command=self.create_save_directory).pack(fill=tk.X, pady=(5, 0))
        
        # 3. Выпадающий список с файлами
        ttk.Label(control_frame, text="Select File:").pack(anchor=tk.W, pady=(0, 5))
        self.file_combo = ttk.Combobox(control_frame, textvariable=self.selected_file)
        self.file_combo.pack(fill=tk.X, pady=(0, 10))
        self.load_files()
        
        # 4. Кнопка Plot Points
        self.plot_btn = ttk.Button(control_frame, text="Plot Points", 
                                  command=self.plot_points)
        self.plot_btn.pack(fill=tk.X, pady=(0, 10))
        
        # 5. Выбор алгоритма
        algo_frame = ttk.LabelFrame(control_frame, text="Algorithm")
        algo_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(algo_frame, text="Jarvis", 
                       variable=self.algorithm_var, value="Jarvis").pack(anchor=tk.W)
        ttk.Radiobutton(algo_frame, text="Graham", 
                       variable=self.algorithm_var, value="Graham").pack(anchor=tk.W)
        
        # 6. Кнопка расчета
        self.calc_btn = ttk.Button(control_frame, text="Calculate", 
                                  command=self.calculate_hull)
        self.calc_btn.pack(fill=tk.X, pady=(0, 10))
        
        # 7. Кнопка сохранения результатов
        self.save_btn = ttk.Button(control_frame, text="Save Results", 
                                  command=self.save_results)
        self.save_btn.pack(fill=tk.X, pady=(0, 10))
        
        # 8. Настройки отображения
        settings_frame = ttk.LabelFrame(control_frame, text="Hull Settings")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Max layers
        ttk.Label(settings_frame, text="Max Layers:").pack(anchor=tk.W)
        ttk.Entry(settings_frame, textvariable=self.max_layers_var).pack(fill=tk.X, pady=(0, 5))
        
        # Plot depth
        ttk.Checkbutton(settings_frame, text="Plot Depth of Points",
                       variable=self.plot_depth_var).pack(anchor=tk.W, pady=(0, 5))
        
        # Кнопка отрисовки
        self.draw_btn = ttk.Button(settings_frame, text="Draw Hulls",
                                  command=self.draw_hulls)
        self.draw_btn.pack(fill=tk.X)
        
        # Кнопка сохранения графика
        self.save_plot_btn = ttk.Button(settings_frame, text="Save Plot",
                                       command=self.save_plot)
        self.save_plot_btn.pack(fill=tk.X, pady=(5, 0))
        
        # Текстовое поле с прокруткой (изначально скрыто)
        self.text_area = scrolledtext.ScrolledText(main_frame, height=15, width=40)
        self.text_area.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        self.text_area.pack_forget()  # Скрываем изначально
        
        # Холст для matplotlib (изначально скрыт)
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_widget.pack_forget()  # Скрываем изначально
        
    def browse_input_directory(self):
        """Открывает диалог выбора директории с данными"""
        directory = filedialog.askdirectory(initialdir=self.directory_var.get())
        if directory:
            self.directory_var.set(directory)
            self.load_files()
    
    def browse_save_directory(self):
        """Открывает диалог выбора директории для сохранения"""
        directory = filedialog.askdirectory(initialdir=self.save_directory_var.get())
        if directory:
            self.save_directory_var.set(directory)
        
    def create_save_directory(self):
        """Создает директорию для сохранения если она не существует"""
        directory = self.save_directory_var.get()
        if directory:
            try:
                os.makedirs(directory, exist_ok=True)
                self.show_message(f"Directory '{directory}' is ready for use!")
            except Exception as e:
                self.show_message(f"Error creating directory: {e}")
        else:
            self.show_message("Please specify a directory path!")
        
    def load_files(self):
        """Загружает список файлов из директории"""
        directory = self.directory_var.get()
        if not os.path.exists(directory):
            self.show_message(f"Directory '{directory}' does not exist!")
            return
            
        try:
            files = [f for f in os.listdir(directory) 
                    if f.endswith(('.txt'))]
            files.sort()  # Сортируем файлы по имени
            
            self.file_combo['values'] = files
            if files:
                self.selected_file.set(files[0])
            else:
                self.selected_file.set('')
                self.show_message(f"No .txt files found in '{directory}'")
                
        except Exception as e:
            self.show_message(f"Error loading files from {directory}: {e}")
    
    def plot_points(self):
        """Отображает точки на графике"""
        filename = self.selected_file.get()
        if not filename:
            self.show_message("Please select a file first!")
            return
            
        try:
            full_path = os.path.join(self.directory_var.get(), filename)
            points = fup.load_points(full_path)
            
            # Показываем холст если был скрыт
            self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
            # Очищаем и рисуем точки
            self.ax.clear()
            x = [p[0] for p in points]
            y = [p[1] for p in points]
            self.ax.scatter(x, y, color='blue', alpha=0.6)
            self.ax.set_title(f"Points from {filename}")
            self.ax.set_xlabel("X")
            self.ax.set_ylabel("Y")
            self.ax.grid(True, alpha=0.3)
            
            # Устанавливаем равные масштабы по осям
            self.ax.set_aspect('equal', adjustable='datalim')
            
            self.canvas.draw()
            
        except Exception as e:
            self.show_message(f"Error plotting points: {e}")
    
    def calculate_hull(self):
        """Вычисляет выпуклую оболочку"""
        algorithm = self.algorithm_var.get()
        filename = self.selected_file.get()
        
        if not filename:
            self.show_message("Please select a file first!")
            return


            
        try:

            input_name = os.path.join(self.directory_var.get(), filename)
            func_depth_path = self.save_directory_var.get() + "/func_depth_" + filename
            output_fname = self.save_directory_var.get() + "/output_hulls_" + filename
            points_depth = self.save_directory_var.get() + "/points_depth_" + filename

            hulls, exetime, func_depth_data = call_cpp(
                input_fname=input_name,
                func_depth=func_depth_path,
                algo=algorithm,
                output_fname=output_fname,
                points_depth=points_depth
            )

            # Показываем текстовое поле если было скрыто
            self.text_area.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
            
            full_path = os.path.join(self.directory_var.get(), filename)
            points = fup.load_points(full_path)
            
            # Имитация расчета
            result_text = f"Algorithm: {algorithm}\n"
            result_text += f"File: {filename}\n"
            result_text += f"Input Directory: {self.directory_var.get()}\n"
            result_text += f"Save Directory: {self.save_directory_var.get()}\n"
            result_text += f"Points: {len(points)}\n"
            result_text += f"M(S): {len(hulls)-1}\n"
            result_text += f"Time: {exetime}\n\n"
            result_text += "Depth Function:\n"

            depths = func_depth_data[:, 1]

            for i in range(len(depths)):
                result_text += f"{i}, {depths[i]}\n"
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, result_text)
            
        except Exception as e:
            self.show_message(f"Error calculating hull: {e}")
    
    def save_results(self):
        """Сохраняет результаты расчета в файл"""
        if not self.save_directory_var.get():
            self.show_message("Please specify a save directory first!")
            return
            
        filename = self.selected_file.get()
        if not filename:
            self.show_message("Please select a file first!")
            return
            
        try:
            # Создаем директорию если не существует
            os.makedirs(self.save_directory_var.get(), exist_ok=True)
            
            # Генерируем имя файла для результатов
            base_name = os.path.splitext(filename)[0]
            result_filename = f"{base_name}_results.txt"
            result_path = os.path.join(self.save_directory_var.get(), result_filename)
            
            # Сохраняем результаты (заглушка)
            with open(result_path, 'w') as f:
                f.write(f"Results for {filename}\n")
                f.write(f"Algorithm: {self.algorithm_var.get()}\n")
                f.write(f"Total points: 100\n")  # Заглушка
                f.write(f"Layers found: 5\n")
                f.write(f"Calculation time: 0.15s\n")
            
            self.show_message(f"Results saved to: {result_path}")
            
        except Exception as e:
            self.show_message(f"Error saving results: {e}")
    
    def save_plot(self):
        """Сохраняет текущий график в файл"""
        if not self.save_directory_var.get():
            self.show_message("Please specify a save directory first!")
            return
            
        filename = self.selected_file.get()
        if not filename:
            self.show_message("Please select a file first!")
            return
            
        try:
            # Создаем директорию если не существует
            os.makedirs(self.save_directory_var.get(), exist_ok=True)
            
            # Генерируем имя файла для графика
            base_name = os.path.splitext(filename)[0]
            plot_filename = f"{base_name}_plot.png"
            plot_path = os.path.join(self.save_directory_var.get(), plot_filename)
            
            # Сохраняем график
            self.fig.savefig(plot_path, dpi=300, bbox_inches='tight')
            self.show_message(f"Plot saved to: {plot_path}")
            
        except Exception as e:
            self.show_message(f"Error saving plot: {e}")
    
    def draw_hulls(self):
        """Отрисовывает оболочки с настройками"""
        try:
            max_layers = int(self.max_layers_var.get())
            plot_depth = self.plot_depth_var.get()
            
            filename = self.selected_file.get()
            if not filename:
                self.show_message("Please select a file first!")
                return
            
            # Показываем холст если был скрыт
            self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
            full_path = os.path.join(self.directory_var.get(), filename)
            points = fup.load_points(full_path)
            
            # Очищаем и рисуем
            self.ax.clear()
            x = [p[0] for p in points]
            y = [p[1] for p in points]
            
            self.ax.scatter(x, y, color='blue', alpha=0.6)
            self.ax.set_title(f"Hulls: {filename} (Max Layers: {max_layers}, Plot Depth: {plot_depth})")
            self.ax.set_xlabel("X")
            self.ax.set_ylabel("Y")
            self.ax.grid(True, alpha=0.3)
            self.ax.set_aspect('equal', adjustable='datalim')
            
            self.canvas.draw()
            
        except ValueError:
            self.show_message("Please enter a valid number for max layers!")
        except Exception as e:
            self.show_message(f"Error drawing hulls: {e}")
    
    def show_message(self, message):
        """Показывает сообщение в текстовом поле"""
        self.text_area.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, message)

def main():
    root = tk.Tk()
    app = ConvexHullGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
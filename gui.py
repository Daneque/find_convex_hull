import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib.widgets import Cursor
from matplotlib.patches import Rectangle
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
        self.directory_var = tk.StringVar(value="Files")
        self.save_directory_var = tk.StringVar(value="Results")
        self.algorithm_var = tk.StringVar(value="Jarvis")
        self.max_layers_var = tk.StringVar(value="10")
        self.plot_depth_var = tk.BooleanVar(value=False)

        # Переменные для хранения данных
        self.points = None
        self.hulls = None
        self.depth_data = None
        self.func_depth_data = None

        # Для интерактивности
        self.cursor = None
        self.annot = None
        self.zoom_rect = None
        self.zoom_start = None
        self.zoom_enabled = False

        self.setup_ui()

    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Левая панель - элементы управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self._setup_directory_controls(control_frame)
        self._setup_save_controls(control_frame)
        self._setup_file_selection(control_frame)
        self._setup_algorithm_controls(control_frame)
        self._setup_hull_settings(control_frame)
        self._setup_zoom_controls(control_frame)

        # Текстовое поле с прокруткой (изначально скрыто)
        self.text_area = scrolledtext.ScrolledText(
            main_frame, height=15, width=40
        )
        self.text_area.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        self.text_area.pack_forget()  # Скрываем изначально

        # Графическая область
        self._setup_graph_area(main_frame)

        # Подключаем обработчики событий для кастомного масштабирования
        self.setup_zoom_handlers()

    def _setup_directory_controls(self, parent):
        """Настраивает элементы управления директорией"""
        dir_frame = ttk.LabelFrame(parent, text="Data Directory")
        dir_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(dir_frame, text="Input Directory:").pack(anchor=tk.W)

        dir_input_frame = ttk.Frame(dir_frame)
        dir_input_frame.pack(fill=tk.X, pady=(5, 0))

        self.dir_entry = ttk.Entry(
            dir_input_frame, textvariable=self.directory_var
        )
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            dir_input_frame, text="Browse",
            command=self.browse_input_directory
        ).pack(side=tk.RIGHT, padx=(5, 0))

        buttons_frame = ttk.Frame(dir_frame)
        buttons_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Button(
            buttons_frame, text="Refresh Files",
            command=self.load_files
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Кнопка для переименования файлов
        ttk.Button(
            buttons_frame, text="Rename Files",
            command=self.rename_files_in_directory
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True)

    def _setup_save_controls(self, parent):
        """Настраивает элементы управления сохранением"""
        save_dir_frame = ttk.LabelFrame(parent, text="Save Directory")
        save_dir_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(save_dir_frame, text="Output Directory:").pack(anchor=tk.W)

        save_dir_input_frame = ttk.Frame(save_dir_frame)
        save_dir_input_frame.pack(fill=tk.X, pady=(5, 0))

        self.save_dir_entry = ttk.Entry(
            save_dir_input_frame, textvariable=self.save_directory_var
        )
        self.save_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            save_dir_input_frame, text="Browse",
            command=self.browse_save_directory
        ).pack(side=tk.RIGHT, padx=(5, 0))

        ttk.Button(
            save_dir_frame, text="Create Directory",
            command=self.create_save_directory
        ).pack(fill=tk.X, pady=(5, 0))

    def _setup_file_selection(self, parent):
        """Настраивает выбор файла"""
        ttk.Label(parent, text="Select File:").pack(anchor=tk.W, pady=(0, 5))
        self.file_combo = ttk.Combobox(
            parent, textvariable=self.selected_file
        )
        self.file_combo.pack(fill=tk.X, pady=(0, 10))
        self.load_files()

        # Кнопка Plot Points
        self.plot_btn = ttk.Button(
            parent, text="Plot Points", command=self.plot_points
        )
        self.plot_btn.pack(fill=tk.X, pady=(0, 10))

    def _setup_algorithm_controls(self, parent):
        """Настраивает выбор алгоритма"""
        algo_frame = ttk.LabelFrame(parent, text="Algorithm")
        algo_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Radiobutton(
            algo_frame, text="Jarvis",
            variable=self.algorithm_var, value="Jarvis"
        ).pack(anchor=tk.W)

        ttk.Radiobutton(
            algo_frame, text="Graham",
            variable=self.algorithm_var, value="Graham"
        ).pack(anchor=tk.W)

        # Кнопка расчета
        self.calc_btn = ttk.Button(
            parent, text="Calculate", command=self.calculate_hull
        )
        self.calc_btn.pack(fill=tk.X, pady=(0, 10))

        # Кнопка сохранения результатов
        self.save_btn = ttk.Button(
            parent, text="Save Results", command=self.save_results
        )
        self.save_btn.pack(fill=tk.X, pady=(0, 10))

    def _setup_hull_settings(self, parent):
        """Настраивает настройки отображения оболочек"""
        settings_frame = ttk.LabelFrame(parent, text="Hull Settings")
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        # Max layers
        ttk.Label(settings_frame, text="Max Layers:").pack(anchor=tk.W)
        ttk.Entry(
            settings_frame, textvariable=self.max_layers_var
        ).pack(fill=tk.X, pady=(0, 5))

        # Plot depth
        self.depth_checkbox = ttk.Checkbutton(
            settings_frame, text="Plot Depth of Points",
            variable=self.plot_depth_var
        )
        self.depth_checkbox.pack(anchor=tk.W, pady=(0, 5))

        # Кнопка отрисовки
        self.draw_btn = ttk.Button(
            settings_frame, text="Draw Hulls", command=self.draw_hulls
        )
        self.draw_btn.pack(fill=tk.X)

        # Кнопка сохранения графика
        self.save_plot_btn = ttk.Button(
            settings_frame, text="Save Plot", command=self.save_plot
        )
        self.save_plot_btn.pack(fill=tk.X, pady=(5, 0))

    def _setup_zoom_controls(self, parent):
        """Настраивает управление масштабированием"""
        zoom_frame = ttk.LabelFrame(parent, text="Zoom Controls")
        zoom_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            zoom_frame, text="Enable Zoom",
            command=self.enable_zoom
        ).pack(fill=tk.X, pady=(5, 2))

        ttk.Button(
            zoom_frame, text="Reset View",
            command=self.reset_view
        ).pack(fill=tk.X, pady=(2, 5))

    def _setup_graph_area(self, parent):
        """Настраивает графическую область"""
        graph_frame = ttk.Frame(parent)
        graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Холст для matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Панель инструментов matplotlib
        self.toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(
            side=tk.TOP, fill=tk.BOTH, expand=True
        )

    def rename_files_in_directory(self):
        """Переименовывает все файлы в выбранной директории"""
        directory = self.directory_var.get()
        
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Error", "Please select a valid directory first!")
            return
        
        # Запрашиваем подтверждение
        result = messagebox.askyesno(
            "Confirm Rename", 
            f"Are you sure you want to rename all files in:\n{directory}\n\n"
            "Files will be renamed to: file1.txt, file2.txt, etc.\n"
            "This action cannot be undone!"
        )
        
        if not result:
            return
        
        try:
            # Получаем список всех файлов в директории
            files = [f for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f))]
            
            # Сортируем файлы для предсказуемого порядка
            files.sort()
            
            if not files:
                messagebox.showinfo("Info", "No files found in the directory.")
                return
            
            # Переименовываем файлы
            renamed_count = 0
            for i, old_filename in enumerate(files, 1):
                # Получаем расширение исходного файла
                _, old_extension = os.path.splitext(old_filename)
                
                # Формируем новое имя
                new_filename = f"file{i}{old_extension}"
                old_path = os.path.join(directory, old_filename)
                new_path = os.path.join(directory, new_filename)
                
                # Пропускаем если имя уже правильное
                if old_filename == new_filename:
                    continue
                
                # Проверяем не существует ли уже файл с таким именем
                if os.path.exists(new_path):
                    continue
                
                # Переименовываем
                os.rename(old_path, new_path)
                renamed_count += 1
            
            # Обновляем список файлов в комбобоксе
            self.load_files()
            
            messagebox.showinfo(
                "Success", 
                f"Successfully renamed {renamed_count} files!\n"
                f"Files are now named: file1{os.path.splitext(files[0])[1]}, file2{os.path.splitext(files[0])[1]}, etc."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error renaming files: {str(e)}")

    def setup_zoom_handlers(self):
        """Настраивает обработчики событий для масштабирования"""
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)

    def enable_zoom(self):
        """Включает режим масштабирования"""
        self.zoom_enabled = True
        self.show_message("Zoom mode enabled. Drag to select area.")

    def disable_zoom(self):
        """Выключает режим масштабирования"""
        self.zoom_enabled = False
        if self.zoom_rect:
            self.zoom_rect.remove()
            self.zoom_rect = None
        self.zoom_start = None

    def reset_view(self):
        """Сбрасывает вид графика к исходному"""
        self.ax.autoscale()
        self.ax.set_aspect('equal', adjustable='datalim')
        self.canvas.draw()
        self.disable_zoom()
        self.show_message("View reset to original")

    def on_press(self, event):
        """Обработчик нажатия кнопки мыши"""
        if not self.zoom_enabled or event.inaxes != self.ax:
            return

        self.zoom_start = (event.xdata, event.ydata)
        self.zoom_rect = Rectangle(
            (0, 0), 0, 0, fill=False,
            edgecolor='red', linewidth=2, alpha=0.8
        )
        self.ax.add_patch(self.zoom_rect)

    def on_motion(self, event):
        """Обработчик движения мыши"""
        if (not self.zoom_enabled or self.zoom_start is None
                or event.inaxes != self.ax):
            return

        start_x, start_y = self.zoom_start
        current_x, current_y = event.xdata, event.ydata

        # Обновляем прямоугольник выделения
        width = current_x - start_x
        height = current_y - start_y

        self.zoom_rect.set_width(width)
        self.zoom_rect.set_height(height)
        self.zoom_rect.set_xy((start_x, start_y))

        self.canvas.draw_idle()

    def on_release(self, event):
        """Обработчик отпускания кнопки мыши"""
        if (not self.zoom_enabled or self.zoom_start is None
                or event.inaxes != self.ax):
            return

        start_x, start_y = self.zoom_start
        end_x, end_y = event.xdata, event.ydata

        # Убеждаемся что координаты валидны
        if (start_x is None or start_y is None
                or end_x is None or end_y is None):
            return

        # Определяем границы зума
        x_min, x_max = sorted([start_x, end_x])
        y_min, y_max = sorted([start_y, end_y])

        # Применяем масштабирование
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

        # Убираем прямоугольник выделения
        if self.zoom_rect:
            self.zoom_rect.remove()
            self.zoom_rect = None

        self.zoom_start = None
        self.canvas.draw()
        self.show_message(
            f"Zoomed to: x[{x_min:.2f}, {x_max:.2f}], "
            f"y[{y_min:.2f}, {y_max:.2f}]"
        )

    def browse_input_directory(self):
        """Открывает диалог выбора директории с данными"""
        directory = filedialog.askdirectory(
            initialdir=self.directory_var.get()
        )
        if directory:
            self.directory_var.set(directory)
            self.load_files()

    def browse_save_directory(self):
        """Открывает диалог выбора директории для сохранения"""
        directory = filedialog.askdirectory(
            initialdir=self.save_directory_var.get()
        )
        if directory:
            self.save_directory_var.set(directory)

    def create_save_directory(self):
        """Создает директорию для сохранения если она не существует"""
        directory = self.save_directory_var.get()
        if directory:
            try:
                os.makedirs(directory, exist_ok=True)
                self.show_message(
                    f"Directory '{directory}' is ready for use!"
                )
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
            files = [
                f for f in os.listdir(directory)
                if f.endswith(('.txt'))
            ]
            files.sort()  # Сортируем файлы по имени

            self.file_combo['values'] = files
            if files:
                self.selected_file.set(files[0])
            else:
                self.selected_file.set('')
                self.show_message(
                    f"No .txt files found in '{directory}'"
                )

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
            self.points = fup.load_points(full_path)

            # Очищаем и рисуем точки
            self.ax.clear()
            x = [p[0] for p in self.points]
            y = [p[1] for p in self.points]
            self.ax.scatter(x, y, color='blue', alpha=0.6)
            self.ax.set_title(f"Points from {filename}")
            self.ax.set_xlabel("X")
            self.ax.set_ylabel("Y")
            self.ax.grid(True, alpha=0.3)

            # Устанавливаем равные масштабы по осям
            self.ax.set_aspect('equal', adjustable='datalim')

            self.canvas.draw()
            self.disable_zoom()

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
            func_depth_path = (
                f"{self.save_directory_var.get()}/func_depth_{filename}"
            )
            output_fname = (
                f"{self.save_directory_var.get()}/output_hulls_{filename}"
            )
            points_depth = (
                f"{self.save_directory_var.get()}/points_depth_{filename}"
            )

            self.hulls, exetime, self.func_depth_data = call_cpp(
                input_fname=input_name,
                func_depth=func_depth_path,
                algo=algorithm,
                output_fname=output_fname,
                points_depth=points_depth
            )

            # Загружаем данные о глубинах точек
            points_depth_path = (
                f"{self.save_directory_var.get()}/points_depth_{filename}"
            )
            if os.path.exists(points_depth_path):
                self.depth_data = np.loadtxt(points_depth_path)

            # Показываем текстовое поле если было скрыто
            self.text_area.pack(
                side=tk.BOTTOM, fill=tk.X, pady=(10, 0)
            )

            full_path = os.path.join(self.directory_var.get(), filename)
            self.points = fup.load_points(full_path)

            # Формируем текст результата
            result_text = f"Algorithm: {algorithm}\n"
            result_text += f"File: {filename}\n"
            result_text += f"Input Directory: {self.directory_var.get()}\n"
            result_text += f"Save Directory: {self.save_directory_var.get()}\n"
            result_text += f"Points: {len(self.points)}\n"
            result_text += f"M(S): {len(self.hulls)-1}\n"
            result_text += f"Time: {exetime}\n\n"
            result_text += "Depth Function:\n"

            depths = self.func_depth_data[:, 1]

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
            result_path = os.path.join(
                self.save_directory_var.get(), result_filename
            )

            # Сохраняем результаты
            with open(result_path, 'w') as f:
                f.write(f"Results for {filename}\n")
                f.write(f"Algorithm: {self.algorithm_var.get()}\n")
                total_points = (
                    len(self.points) if self.points is not None else 'N/A'
                )
                f.write(f"Total points: {total_points}\n")
                layers_found = (
                    len(self.hulls)-1 if self.hulls is not None else 'N/A'
                )
                f.write(f"Layers found: {layers_found}\n")
                if self.func_depth_data is not None:
                    f.write("Depth function values:\n")
                    for i, depth in enumerate(self.func_depth_data[:, 1]):
                        f.write(f"  Point {i}: {depth}\n")

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
            plot_path = os.path.join(
                self.save_directory_var.get(), plot_filename
            )

            # Сохраняем график
            self.fig.savefig(plot_path, dpi=300, bbox_inches='tight')
            self.show_message(f"Plot saved to: {plot_path}")

        except Exception as e:
            self.show_message(f"Error saving plot: {e}")

    def draw_hulls(self):
        """Отрисовывает оболочки с настройками прямо в GUI"""
        try:
            max_layers = int(self.max_layers_var.get())
            plot_depth = self.plot_depth_var.get()

            filename = self.selected_file.get()
            if not filename:
                self.show_message("Please select a file first!")
                return

            if self.hulls is None:
                self.show_message(
                    "Please calculate hulls first using 'Calculate' button!"
                )
                return

            # Ограничиваем количество слоев если указано
            layers_to_plot = (
                self.hulls[:max_layers] if max_layers else self.hulls
            )

            # Очищаем график
            self.ax.clear()

            # Цвета для разных слоев (от темного к светлому)
            colors = plt.cm.viridis(
                np.linspace(0, 0.8, len(layers_to_plot))
            )

            # Рисуем все исходные точки
            if self.points is not None:
                x_all = [p[0] for p in self.points]
                y_all = [p[1] for p in self.points]
                self.ax.scatter(
                    x_all, y_all, c='lightgray', s=30, alpha=0.7,
                    label='All points'
                )

            # Рисуем каждый слой
            for i, layer in enumerate(layers_to_plot):
                if len(layer) == 0:
                    continue

                color = colors[i]
                layer_label = f'Layer {i+1} ({len(layer)} points)'

                # Рисуем точки слоя
                x_layer = [p[0] for p in layer]
                y_layer = [p[1] for p in layer]
                self.ax.scatter(
                    x_layer, y_layer, c=[color], s=80, alpha=1.0,
                    label=layer_label, zorder=3
                )

                # Рисуем выпуклую оболочку (замкнутую)
                if len(layer) > 1:
                    # Замыкаем оболочку
                    closed_layer = np.vstack([layer, layer[0]])
                    self.ax.plot(
                        closed_layer[:, 0], closed_layer[:, 1],
                        color=color, linewidth=3, alpha=0.9, zorder=2
                    )

            # Настройки графика
            title = f"Onion Decomposition ({len(self.hulls)} layers total)"
            if max_layers:
                title = f"{title} (showing first {max_layers} layers)"

            self.ax.set_title(title)
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            # self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            self.ax.grid(True, alpha=0.3)
            self.ax.set_aspect('equal', adjustable='datalim')

            # Добавляем отображение глубины при наведении
            if plot_depth and self.depth_data is not None:
                self.setup_depth_interactivity()
            else:
                # Убираем интерактивность если не нужно
                if hasattr(self, '_cursor_connection'):
                    self.canvas.mpl_disconnect(self._cursor_connection)
                if self.annot:
                    self.annot.set_visible(False)

            self.canvas.draw()
            self.disable_zoom()

        except ValueError:
            self.show_message("Please enter a valid number for max layers!")
        except Exception as e:
            self.show_message(f"Error drawing hulls: {e}")

    def setup_depth_interactivity(self):
        """Настраивает интерактивное отображение глубины точек"""
        # Создаем курсор
        self.cursor = Cursor(
            self.ax, useblit=True, color='red', linewidth=1
        )

        # Создаем аннотацию
        self.annot = self.ax.annotate(
            "", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w", alpha=0.8),
            arrowprops=dict(arrowstyle="->")
        )
        self.annot.set_visible(False)

        def update_annot(event):
            if event.inaxes == self.ax:
                # Ищем ближайшую точку
                distances = np.sqrt(
                    (self.depth_data[:, 0] - event.xdata)**2 +
                    (self.depth_data[:, 1] - event.ydata)**2
                )
                idx = np.argmin(distances)

                # Если точка достаточно близко
                if distances[idx] < 0.5:  # порог расстояния
                    x, y, depth = self.depth_data[idx]
                    self.annot.xy = (x, y)
                    self.annot.set_text(f"Depth: {int(depth)}")
                    self.annot.set_visible(True)
                    self.canvas.draw_idle()
                else:
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()

        # Подключаем обработчик событий
        self._cursor_connection = self.canvas.mpl_connect(
            "motion_notify_event", update_annot
        )

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
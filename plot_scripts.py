import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

def load_depth_data_no_header(filename):
    """
    Загружает данные о глубинах точек из файла без заголовка
    Формат файла: x y D(p)
    """
    data = np.loadtxt(filename)
    return data

def plot_onion_decomposition(layers, points=None, max_layers=None, show_depth=False, depth_fname=None):
    """
    Рисует onion decomposition (вложенные выпуклые оболочки)
    
    Parameters:
    -----------
    layers : list of np.array
        Список оболочек, каждая оболочка - np.array формы (N, 2)
    points : np.array, optional
        Исходные точки для отображения
    max_layers : int, optional
        Максимальное количество слоев для отображения (по умолчанию все)
    show_depth : bool, optional
        Показывать глубину точек при наведении
    depth_fname : str, optional
        Путь к файлу с данными о глубинах точек
    """
    
    # Загружаем данные о глубинах если указан файл
    depth_data = None
    if depth_fname is not None:
        try:
            depth_data = load_depth_data_no_header(depth_fname)
        except Exception as e:
            print(f"Warning: Could not load depth data from {depth_fname}: {e}")

    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Ограничиваем количество слоев если указано
    if max_layers is not None:
        layers_to_plot = layers[:max_layers]
    else:
        layers_to_plot = layers
    
    # Цвета для разных слоев (от темного к светлому)
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(layers_to_plot)))

    # ВСЕГДА рисуем все исходные точки
    if points is not None:
        plt.scatter(points[:, 0], points[:, 1], 
                   c='lightgray', s=30, alpha=0.7, label='All points')
    
    # Рисуем каждый слой
    for i, layer in enumerate(layers_to_plot):
        if len(layer) == 0:
            continue
            
        color = colors[i]
        layer_label = f'Layer {i+1} ({len(layer)} points)'
        
        # Рисуем точки слоя поверх всех точек
        plt.scatter(layer[:, 0], layer[:, 1], 
                   c=[color], s=80, alpha=1.0, label=layer_label, zorder=3)
        
        # Рисуем выпуклую оболочку (замкнутую)
        if len(layer) > 1:
            # Замыкаем оболочку (добавляем первую точку в конец)
            closed_layer = np.vstack([layer, layer[0]])
            plt.plot(closed_layer[:, 0], closed_layer[:, 1], 
                    color=color, linewidth=3, alpha=0.9, zorder=2)
            
            # Заливка для оболочки (прозрачная)
            plt.fill(closed_layer[:, 0], closed_layer[:, 1], 
                    color=color, alpha=0.2, zorder=1)
    
    # Добавляем отображение глубины при наведении
    if show_depth and depth_data is not None:
        # Создаем курсор
        cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
        
        # Создаем аннотацию
        annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                           bbox=dict(boxstyle="round", fc="w", alpha=0.8),
                           arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)
        
        def update_annot(event):
            if event.inaxes == ax:
                # Ищем ближайшую точку
                distances = np.sqrt((depth_data[:, 0] - event.xdata)**2 + 
                                  (depth_data[:, 1] - event.ydata)**2)
                idx = np.argmin(distances)
                
                # Если точка достаточно близко
                if distances[idx] < 0.5:  # порог расстояния
                    x, y, depth = depth_data[idx]
                    annot.xy = (x, y)
                    annot.set_text(f"Depth: {int(depth)}")
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
        
        fig.canvas.mpl_connect("motion_notify_event", update_annot)
    
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # Формируем заголовок
    title = f"Onion Decomposition ({len(layers)} layers total)"
    if max_layers is not None:
        title = f"{title} (showing first {max_layers} layers)"
    
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
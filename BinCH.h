#ifndef BINCH_H
#define BINCH_H

#include "Point.h"
#include <vector>

class BinCH {
private:
    std::vector<std::vector<Point>> layers;
    size_t N_layers;

public:
    // Конструкторы
    BinCH();  // Пустой конструктор
    BinCH(const std::vector<std::vector<Point>>& initial_layers);  // Конструктор с вектор векторов
    
    // Методы доступа
    size_t getNLayers() const;
    const std::vector<std::vector<Point>>& getLayers() const;
    const std::vector<Point>& getLayer(size_t index) const;
    
    // Методы модификации
    void addLayer(const std::vector<Point>& new_layer);
    void addLayer(std::vector<Point>&& new_layer);  // Для перемещения
    
    // Вспомогательные методы
    void clear();
    bool isEmpty() const;
    size_t totalPoints() const;
    
    // Отладочный метод
    void printInfo() const;
};

#endif // BINCH_H
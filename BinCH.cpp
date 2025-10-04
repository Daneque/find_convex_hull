#include "BinCH.h"
#include <iostream>

// Пустой конструктор
BinCH::BinCH() : N_layers(0) {}

// Конструктор с вектор векторов
BinCH::BinCH(const std::vector<std::vector<Point>>& initial_layers) 
    : layers(initial_layers), N_layers(initial_layers.size()) {}

// Получить количество слоев
size_t BinCH::getNLayers() const {
    return N_layers;
}

// Получить все слои (константная ссылка)
const std::vector<std::vector<Point>>& BinCH::getLayers() const {
    return layers;
}

// Получить конкретный слой по индексу
const std::vector<Point>& BinCH::getLayer(size_t index) const {
    if (index >= N_layers) {
        throw std::out_of_range("Index out of range in BinCH::getLayer");
    }
    return layers[index];
}

// Добавить новый слой (копирование)
void BinCH::addLayer(const std::vector<Point>& new_layer) {
    layers.push_back(new_layer);
    N_layers = layers.size();
}

// Добавить новый слой (перемещение)
void BinCH::addLayer(std::vector<Point>&& new_layer) {
    layers.push_back(std::move(new_layer));
    N_layers = layers.size();
}

// Очистить все слои
void BinCH::clear() {
    layers.clear();
    N_layers = 0;
}

// Проверить пустоту
bool BinCH::isEmpty() const {
    return N_layers == 0;
}

// Подсчитать общее количество точек во всех слоях
size_t BinCH::totalPoints() const {
    size_t count = 0;
    for (const auto& layer : layers) {
        count += layer.size();
    }
    return count;
}

// Отладочная информация
void BinCH::printInfo() const {
    std::cout << "BinCH Info:" << std::endl;
    std::cout << "Number of layers: " << N_layers << std::endl;
    std::cout << "Total points: " << totalPoints() << std::endl;
    
    for (size_t i = 0; i < N_layers; ++i) {
        std::cout << "Layer " << i << ": " << layers[i].size() << " points" << std::endl;
    }
}
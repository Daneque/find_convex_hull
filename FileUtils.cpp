#include "FileUtils.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <string>
#include "Point.h"


// std::vector<Point> readPointsFromFile(const std::string& filename) {
//     std::ifstream file(filename);
//     std::vector<Point> points;

//     if (!file.is_open()) {
//         std::cerr << "Ошибка: не удалось открыть файл " << filename << "\n";
//         return points;
//     }

//     std::string line;
//     while (std::getline(file, line)) {
//         std::stringstream ss(line);
//         std::string x_str, y_str;

//         if (std::getline(ss, x_str, ',') && std::getline(ss, y_str)) {
//             points.emplace_back(std::stod(x_str), std::stod(y_str));
//         }
//     }

//     return points;
// }

std::vector<Point> readPointsFromFile(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<Point> points;

    if (!file.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << filename << "\n";
        return points;
    }

    // Пропускаем первую строку с количеством элементов
    std::string firstLine;
    std::getline(file, firstLine);

    // Читаем остальные строки с точками
    double x, y;
    while (file >> x >> y) {
        points.emplace_back(x, y);
    }

    return points;
}


void savePointsToFile(const std::vector<Point>& points, const std::string& filename) {
    std::ofstream file(filename);

    if (!file.is_open()) {
        throw std::runtime_error("Не удалось открыть файл: " + filename);
    }

    for (const auto& p : points) {
        file << p.getX() << ", " << p.getY() << "\n";
    }

    file.close();
}

void saveHullsToFile(const std::vector<std::vector<Point>>& points, const std::string& filename, long long microsec) {
    std::ofstream file(filename);

    // Записываем время выполнения
    file << "Execution time: " << (microsec / 1000000.0) << " seconds\n\n";

    // Записываем оболочки
    for(int i = 1; i < points.size() + 1; i++){
        file << "Hull " << i << "\n";
        for(const auto& p : points[i-1]){
            file << p.getX() << ", " << p.getY() << "\n";
        }
        file << "\n";
    }

    file.close();
}

void saveLayerStatistics(const std::vector<std::vector<Point>>& layers, const std::string& filename) {
    std::ofstream file(filename);

    // Записываем данные для каждого слоя
    for (size_t i = 0; i < layers.size(); i++) {
        file << (i + 1) << " " << layers[i].size() << "\n";
    }
    
    file.close();
}

void savePointsDepth(const std::vector<std::vector<Point>>& layers, const std::string& filename) {
    std::ofstream file(filename);
    
    // Проходим по всем слоям и вычисляем глубину для каждой точки
    for (int layer_index = 0; layer_index < layers.size(); layer_index++) {
        for (const auto& point : layers[layer_index]) {
            // Глубина точки = номер слоя + 1 (так как слои нумеруются с 0)
            int depth = layer_index;
            file << point.getX() << " " << point.getY() << " " << depth << "\n";
        }
    }
    
    file.close();
}

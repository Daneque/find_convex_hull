#include "FileUtils.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <string>
#include "Point.h"


std::vector<Point> readPointsFromFile(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<Point> points;

    if (!file.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << filename << "\n";
        return points;
    }

    std::string line;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string x_str, y_str;

        if (std::getline(ss, x_str, ',') && std::getline(ss, y_str)) {
            points.emplace_back(std::stod(x_str), std::stod(y_str));
        }
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

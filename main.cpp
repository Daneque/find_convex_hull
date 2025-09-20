#include <iostream>
#include "Point.h"
#include "FileUtils.h"
#include "Tools.h"
#include "FindConv.h"

int main() {
    auto points = readPointsFromFile("points.txt");

    std::cout << "Points:\n";
    for (const auto& p : points) {
        std::cout << p.toString() << "\n";
    }

    std::cout << "Convex hull:\n";
    std::vector<Point> hull = Jarvis(points).first;
    for (const auto& p : hull) {
        std::cout << p.toString() << "\n";
    }
}

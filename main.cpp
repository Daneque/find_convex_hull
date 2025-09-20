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

    Point q(1, 1), w(2, 2);
    std::vector<Point> line = {Point(0,0), Point(1,0)};
    std::cout << "Cosine between " << q.toString() << " and " << w.toString()
              << " = " << cosine_along_line(q, w, line) << "\n";

    auto hull = Jarvis(points);
}

#include <iostream>
#include "Point.h"
#include "FileUtils.h"
#include "Tools.h"
#include "FindConv.h"

int main() {
    auto points = readPointsFromFile("points.txt");
    std::vector<std::vector<Point>> hulls = Onion(points, "Graham");

    saveHullsToFile(hulls, "output_hulls.txt");
    // std::vector<Point> hull = Jarvis(points, ).first;
    // std::cout << "Hull size = " << hull.size()-1 << std::endl;
    // savePointsToFile(hull, "output_points.txt");
    // Point p = Point(0, 0);
    // Point q = Point(1, 1);
    // std::pair pq = {p, q};
    // Point z = Point(2, 2);
    // std::cout << rotate(pq, z) << std::endl;
}

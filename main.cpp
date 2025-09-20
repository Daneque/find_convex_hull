#include <iostream>
#include "Point.h"
#include "FileUtils.h"
#include "Tools.h"
#include "FindConv.h"

int main() {
    auto points = readPointsFromFile("points.txt");
    std::vector<Point> hull = Jarvis(points).first;
    std::cout << "Hull size = " << hull.size()-1 << std::endl;
    savePointsToFile(hull, "output_points.txt");
}

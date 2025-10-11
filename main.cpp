#include <iostream>
#include <algorithm>
#include <chrono>
#include "Point.h"
#include "FileUtils.h"
#include "Tools.h"
#include "FindConv.h"
#include "Chazelle.h"
#include "ChazelleTest.h"
#include "BinCH.h"



int main(int argc, char* argv[]) {
    
    std::string input_file = argv[1];
    std::string algorithm = argv[2];
    std::string func_depth = argv[3];
    std::string output_file = argv[4];
    std::string points_depth = argv[5];

    

    auto points = readPointsFromFile(input_file);

    // Замер времени начала
    auto start = std::chrono::high_resolution_clock::now();
    auto hulls = Onion(points, algorithm);
    
    // Замер времени перед сохранением (исключаем время I/O)
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    saveHullsToFile(hulls, output_file, duration.count());

    saveLayerStatistics(hulls, func_depth);

    savePointsDepth(hulls, points_depth);

    return 0;
    
}

    // std::vector<BinCH> bins = Chazell(points);//GetBins(points);

    // std::vector<std::vector<Point>> smallhulls;

    // for(auto b : bins){
    //     for(size_t i = 0; i < b.getNLayers(); i++){
    //         auto bin_points = b.getLayer(i);
    //         auto hull = SmallHull(bin_points);
    //         smallhulls.push_back(hull);
    //     }
    // }

    // std::cout << bins[0].getNLayers();

    // saveHullsToFile(smallhulls, "smallhulls.txt");

    // for(auto b : bins) {
    //     b.printInfo();
    //     for(size_t i = 0; i < b.getNLayers(); i++){
    //         b.printLayer(i);
    //     }
    // }

    // std::cout << points[0].getX() << " " << points[0].getY() << std::endl;
    // std::cout << points.size();

    // auto onion_layers = ChazelleTest::onionDecomposition(points);

    // saveHullsToFile(onion_layers, "output_hulls.txt");

    // auto onions = Onion(points, "Jarvis");

    // saveHullsToFile(onions, "output_hulls2.txt");

    // std::sort(points.begin(), points.end(), [](const Point& a, const Point& b) {
    // if (a.getX() == b.getX()) 
    //     return a.getY() < b.getY();
    // return a.getX() < b.getX();
    // });

    // std::vector<std::vector<Point>> subsets = splitPoints(points);


    // for(auto v : subsets){
    //     std::cout << "subset ";
    //     for(int i = 0; i < v.size(); i++) {
    //         std::cout << "(" << v[i].getX() << ", " << v[i].getY() << ")" << " | ";
    //     };
    //     std::cout << std::endl;
    // };

    // std::vector<std::vector<Point>> hulls = Onion(points, "Graham");

    // saveHullsToFile(hulls, "output_hulls.txt");
    // std::vector<Point> hull = Jarvis(points, ).first;
    // std::cout << "Hull size = " << hull.size()-1 << std::endl;
    // savePointsToFile(hull, "output_points.txt");
    // Point p = Point(0, 0);
    // Point q = Point(1, 1);
    // std::pair pq = {p, q};
    // Point z = Point(2, 2);
    // std::cout << rotate(pq, z) << std::endl;


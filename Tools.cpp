#include "Tools.h"
#include <cmath>
#include <algorithm>
#include <utility>
#include <iostream>

double dot(const Point& p1, const Point& p2) {
    Point z = p1 * p2;
    return z.getX() + z.getY();
}

double norm(const Point& p) {
    Point z = p * p;
    return std::sqrt(z.getX() + z.getY());
}

double dist(const Point& p, const Point& q) {
    return norm(q - p);
}

double cosine_along_line(const Point& p, const Point& q, const std::pair<Point, Point>& line) {
    Point v1 = q - p;
    Point v2 = line.second - line.first;

    double norm_v1 = norm(v1); 
    double norm_v2 = norm(v2);

    if ((norm_v1 == 0) || (norm_v2 == 0)) {
        std::cout << "Zero norm!\nNorm v1 = " << norm_v1 << ", Norm v2 = " << norm_v2 << "\n";
    }

    double scalar_product = dot(v1, v2);
    return scalar_product / (norm_v1 * norm_v2);
}

template <typename T>
void print_vector(std::vector<T>& vect) {
    for(size_t i = 0; i < vect.size(); i++) {
        std::cout << vect[i] << std::endl;
    }
}


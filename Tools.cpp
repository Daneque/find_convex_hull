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

std::pair<double, size_t> new_point_convex_hull(std::vector<Point>& points, Point& curr_point, size_t curr_idx, std::pair<Point, Point>& direction) {

    std::vector<double> cosines = {};

    for(size_t i = 0; i < points.size(); i++) {
        if (i == curr_idx) {
            cosines.push_back(-3);
            continue;
        }
        cosines.push_back(cosine_along_line(curr_point, points[i], direction));
    }


    auto max_cos_it = std::max_element(cosines.begin(), cosines.end());

    size_t max_cos_idx = std::distance(cosines.begin(), max_cos_it);

    double max_cos = cosines[max_cos_idx];


    std::vector<size_t> max_idxs = {};

    for(size_t i = 0; i < cosines.size(); i++) {
        if (std::abs(cosines[i] - max_cos) < 1e-10) {
            max_idxs.push_back(i);
        }
    }

    if (max_idxs.size() > 1) {
        std::vector<double> lens = {};

        for(size_t i = 0; i < max_idxs.size(); i++) {
            lens.push_back(dist(curr_point, points[max_idxs[i]]));
        }


        auto max_len_it = std::max_element(lens.begin(), lens.end());
        size_t max_len_idx = std::distance(lens.begin(), max_len_it);

        return std::make_pair(cosines[max_idxs[max_len_idx]], max_idxs[max_len_idx]);

    } else {
        return std::make_pair(max_cos, max_cos_idx);
    }

    



}
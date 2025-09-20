#include "FindConv.h"
#include "Tools.h"
#include <cmath>
#include <algorithm>
#include <utility>
#include <iostream>

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

// Заглушка алгоритма Джарвиса
std::vector<Point> Jarvis(const std::vector<Point>& points) {
    std::vector<Point> hull;
    // Реализация алгоритма сюда
    std::cout << "Jarvis algorithm placeholder\n";
    return hull;
}

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


std::pair<std::vector<Point>, std::vector<size_t>> Jarvis(std::vector<Point>& points) {

    std::vector<double> ys = {};

    for(size_t i = 0; i < points.size(); i++) {
        ys.push_back(points[i].getY());
    }

    auto min_y_point = std::min_element(ys.begin(), ys.end());

    size_t min_y_idx = std::distance(ys.begin(), min_y_point);
    size_t curr_idx = min_y_idx;
    Point curr_point = points[min_y_idx];
    std::pair<Point, Point> direction = {Point(0, 0), Point(1, 0)};

    std::vector<Point> hull = {curr_point};
    std::vector<size_t> hull_idxs = {curr_idx};

    do {
        size_t maxcos_idx = new_point_convex_hull(points, curr_point, curr_idx, direction).second;
        curr_idx = maxcos_idx;
        direction = {curr_point, points[curr_idx]};
        curr_point = points[curr_idx];

        hull.push_back(curr_point);
        hull_idxs.push_back(curr_idx);
    } while (!(curr_point == hull[0]));

    return {hull, hull_idxs};


}

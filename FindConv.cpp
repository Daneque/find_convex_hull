#include "FindConv.h"
#include "Tools.h"
#include <cmath>
#include <algorithm>
#include <utility>
#include <iostream>

// std::pair<double, size_t> new_point_convex_hull(std::vector<Point>& points, Point& curr_point, size_t curr_idx, std::pair<Point, Point>& direction) {

//     std::vector<double> cosines = {};

//     for(size_t i = 0; i < points.size(); i++) {

//         if (i == curr_idx) {
//             cosines.push_back(-3);
//             continue;
//         }

//         cosines.push_back(cosine_along_line(curr_point, points[i], direction));
//     }


//     auto max_cos_it = std::max_element(cosines.begin(), cosines.end());

//     size_t max_cos_idx = std::distance(cosines.begin(), max_cos_it);

//     double max_cos = cosines[max_cos_idx];


//     std::vector<size_t> max_idxs = {};

//     for(size_t i = 0; i < cosines.size(); i++) {
//         if (std::abs(cosines[i] - max_cos) < 1e-10) {
//             max_idxs.push_back(i);
//         }
//     }

//     if (max_idxs.size() > 1) {
//         std::vector<double> lens = {};

//         for(size_t i = 0; i < max_idxs.size(); i++) {
//             lens.push_back(dist(curr_point, points[max_idxs[i]]));
//         }


//         auto max_len_it = std::max_element(lens.begin(), lens.end());
//         size_t max_len_idx = std::distance(lens.begin(), max_len_it);

//         return std::make_pair(cosines[max_idxs[max_len_idx]], max_idxs[max_len_idx]);

//     } else {
//         return std::make_pair(max_cos, max_cos_idx);
//     }

// }

std::pair<double, size_t> new_point_convex_hull(
    std::vector<Point>& points,
    Point& curr_point,
    size_t curr_idx,
    std::pair<Point, Point>& direction
) {
    constexpr double EPS = 1e-10;

    double best_cos = -2.0;   // меньше любого возможного косинуса
    double best_len = -1.0;   // для разрешения равных косинусов
    size_t best_idx = curr_idx;

    for (size_t i = 0; i < points.size(); ++i) {
        if (i == curr_idx) continue;

        double c = cosine_along_line(curr_point, points[i], direction);
        double d = dist(curr_point, points[i]);

        if (c > best_cos + EPS) {
            // нашли лучший косинус
            best_cos = c;
            best_len = d;
            best_idx = i;
        } else if (std::abs(c - best_cos) <= EPS && d > best_len) {
            // равные косинусы → выбираем дальнюю точку
            best_len = d;
            best_idx = i;
        }
    }

    return {best_cos, best_idx};
}


std::pair<std::vector<Point>, std::vector<size_t>> Jarvis(std::vector<Point>& points) {
    if (points.size() < 3) {
        return {points, {}};
    }

    // найти индекс точки с минимальным Y
    size_t min_y_idx = 0;
    for (size_t i = 1; i < points.size(); ++i) {
        if (points[i].getY() < points[min_y_idx].getY()) {
            min_y_idx = i;
        }
    }

    size_t curr_idx = min_y_idx;
    Point curr_point = points[min_y_idx];
    std::pair<Point, Point> direction = {Point(0, 0), Point(1, 0)};

    std::vector<Point> hull = {curr_point};
    std::vector<size_t> hull_idxs = {curr_idx};

    do {
        auto [cos_val, next_idx] = new_point_convex_hull(points, curr_point, curr_idx, direction);

        curr_idx = next_idx;
        direction = {curr_point, points[curr_idx]};
        curr_point = points[curr_idx];

        hull.push_back(curr_point);
        hull_idxs.push_back(curr_idx);
    } while (curr_idx != min_y_idx);

    return {hull, hull_idxs};
}



double rotate(Point& a, Point& b, Point& c) {
    return (b.getX() - a.getX()) * (c.getY() - a.getY()) -
           (b.getY() - a.getY()) * (c.getX() - a.getX());
}


// 

std::pair<std::vector<Point>, std::vector<size_t>> Graham(std::vector<Point>& points) {
    constexpr double EPS = 1e-10;

    if (points.size() < 3) {
        return {points, {}};
    }

    // найти нижнюю левую точку (min_y, при равенстве min_x)
    size_t p_min_idx = 0;
    for (size_t i = 1; i < points.size(); ++i) {
        if (points[i].getY() < points[p_min_idx].getY() - EPS ||
           (std::abs(points[i].getY() - points[p_min_idx].getY()) < EPS &&
            points[i].getX() < points[p_min_idx].getX())) {
            p_min_idx = i;
        }
    }

    Point min_p = points[p_min_idx];

    // индексы всех точек
    std::vector<size_t> indices(points.size());
    for (size_t i = 0; i < points.size(); ++i) indices[i] = i;
    std::swap(indices[0], indices[p_min_idx]);

    // направление для косинусов
    std::pair<Point, Point> direction = {Point(0, 0), Point(1, 0)};

    // косинусы и расстояния
    std::vector<double> cosines(points.size()), dists(points.size());
    for (size_t i = 0; i < points.size(); ++i) {
        if (i == p_min_idx) {
            cosines[i] = -2.0;  // заведомо минимальный косинус
            dists[i] = 0.0;
        } else {
            cosines[i] = cosine_along_line(min_p, points[i], direction);
            dists[i]   = dist(min_p, points[i]);
        }
    }

    // сортировка по углу (косинусу), при равенстве — по расстоянию
    std::sort(indices.begin() + 1, indices.end(), [&](size_t i1, size_t i2) {
        if (std::abs(cosines[i1] - cosines[i2]) > EPS) {
            return cosines[i1] > cosines[i2];
        }
        return dists[i1] < dists[i2];
    });

    // построение оболочки
    std::vector<Point> hull = {points[indices[0]], points[indices[1]]};
    std::vector<size_t> hull_idxs = {indices[0], indices[1]};

    for (size_t i = 2; i < indices.size(); ++i) {
        Point next = points[indices[i]];
        size_t next_idx = indices[i];

        while (hull.size() >= 2) {
            Point p1 = hull[hull.size() - 2];
            Point p2 = hull[hull.size() - 1];

            double rot = rotate(p1, p2, next);

            if (rot > EPS) {  // левый поворот
                break;
            } else if (rot < -EPS) {  // правый поворот
                hull.pop_back();
                hull_idxs.pop_back();
            } else {  // на одной прямой
                if (dist(p1, next) > dist(p1, p2)) {
                    hull.pop_back();
                    hull_idxs.pop_back();
                }
                break;
            }
        }

        hull.push_back(next);
        hull_idxs.push_back(next_idx);
    }

    // если нужна замкнутая оболочка — оставляем
    hull.push_back(hull[0]);
    hull_idxs.push_back(hull_idxs[0]);

    return {hull, hull_idxs};
}


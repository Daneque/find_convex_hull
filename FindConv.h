#pragma once
#include <vector>
#include "Point.h"


std::pair<double, size_t> new_point_convex_hull(std::vector<Point>& points, Point& curr_point, size_t curr_idx, std::pair<Point, Point>& direction);
std::pair<std::vector<Point>, std::vector<size_t>> Jarvis(std::vector<Point>& points);
double rotate(std::pair<Point, Point>& direction, Point& p);

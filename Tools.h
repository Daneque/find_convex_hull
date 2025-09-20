#pragma once
#include <vector>
#include "Point.h"

double dot(const Point& p1, const Point& p2);
double norm(const Point& p);
double dist(const Point& p, const Point& q);
double cosine_along_line(const Point& p, const Point& q, const std::pair<Point, Point>& line);
template <typename T>
void print_vector(std::vector<T>& vect);
std::pair<double, size_t> new_point_convex_hull(std::vector<Point>& points, Point& curr_point, size_t curr_idx, std::pair<Point, Point>& direction);

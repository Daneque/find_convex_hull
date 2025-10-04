#pragma once
#include <vector>
#include "Point.h"
#include "BinCH.h"

size_t getLeftmostPoint(std::vector<Point>& hull);
size_t getRightmostPoint(std::vector<Point>& hull);
std::pair<size_t, size_t> getUpperTangent(std::vector<Point>& left_hull, std::vector<Point>& right_hull);
std::pair<size_t, size_t> getLowerTangent(std::vector<Point>& left_hull, std::vector<Point>& right_hull);
std::vector<std::vector<Point>> splitPoints(const std::vector<Point>& points);
void MergeConvHull(std::vector<Point>& chl, std::vector<Point>& chr);
std::vector<BinCH> GetBins(std::vector<Point>& points);
#pragma once
#include <string>
#include <vector>
#include "Point.h"

std::vector<Point> readPointsFromFile(const std::string& filename);
void savePointsToFile(const std::vector<Point>& points, const std::string& filename);
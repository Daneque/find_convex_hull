#pragma once
#include <string>
#include <vector>
#include "Point.h"

std::vector<Point> readPointsFromFile(const std::string& filename);
void savePointsToFile(const std::vector<Point>& points, const std::string& filename);
void saveHullsToFile(const std::vector<std::vector<Point>>& points, const std::string& filename, long long microsec);
void saveLayerStatistics(const std::vector<std::vector<Point>>& layers, const std::string& filename);
void savePointsDepth(const std::vector<std::vector<Point>>& layers, const std::string& filename);
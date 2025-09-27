#include "FileUtils.h"
#include "FindConv.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <string>
#include "Point.h"

size_t getLeftmostPoint(std::vector<Point>& hull) {
    size_t idx = 0;
    for(size_t i = 1; i < hull.size(); i++) {
        if(hull[i].getX() < hull[idx].getX()) {
            idx = i;
        }
    }
    return idx;
}

size_t getRightmostPoint(std::vector<Point>& hull) {
    size_t idx = 0;
    for(size_t i = 1; i < hull.size(); i++) {
        if(hull[i].getX() > hull[idx].getX()) {
            idx = i;
        }
    }
    return idx;
}

std::pair<size_t, size_t> getUpperTangent(std::vector<Point>& left_hull, std::vector<Point>& right_hull) {
    size_t U_L = getRightmostPoint(left_hull);
    size_t U_R = getLeftmostPoint(right_hull);

    size_t L = left_hull.size();
    size_t R = right_hull.size();

    bool flag_left = true;
    bool flag_right = true;

    while (flag_left || flag_right) {

        // проверяем точку в левой ВО
        size_t next_left = (U_L + 1) % L;
        if (rotate(right_hull[U_R], left_hull[U_L], left_hull[next_left]) > 0) {
            U_L = next_left;
        } else {
            flag_left = false;
        }

        // проверяем точку в правой ВО
        size_t prev_right = (U_R + R - 1) % R;
        if (rotate(left_hull[U_L], right_hull[U_R], right_hull[prev_right]) < 0) {
            U_R = prev_right;
        } else {
            flag_right = false;
        }
    }

    return {U_L, U_R};
}

std::pair<size_t, size_t> getLowerTangent(std::vector<Point>& left_hull, std::vector<Point>& right_hull) {
    size_t U_L = getRightmostPoint(left_hull);
    size_t U_R = getLeftmostPoint(right_hull);

    size_t L = left_hull.size();
    size_t R = right_hull.size();

    bool flag_left = true;
    bool flag_right = true;

    while (flag_left || flag_right) {

        // проверяем точку в левой ВО
        size_t next_left = (U_L + L - 1) % L;
        if (rotate(right_hull[U_R], left_hull[U_L], left_hull[next_left]) < 0) {
            U_L = next_left;
        } else {
            flag_left = false;
        }

        // проверяем точку в правой ВО
        size_t prev_right = (U_R + 1) % R;
        if (rotate(left_hull[U_L], right_hull[U_R], right_hull[prev_right]) > 0) {
            U_R = prev_right;
        } else {
            flag_right = false;
        }
    }

    return {U_L, U_R};
}

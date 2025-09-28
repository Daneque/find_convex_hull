#include "Chazelle.h"
#include "FileUtils.h"
#include "FindConv.h"
#include <vector>
#include <string>
#include "Point.h"
#include "Tools.h"
#include <algorithm>
#include <cmath>
#include <iostream>


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

    if(L == 1 && R == 1) {return {0, 0};}

    bool not_one_left = L > 1 ? true : false;
    bool not_one_right = R > 1 ? true : false;

    bool flag_left = true;
    bool flag_right = true;

    while (flag_left || flag_right) {

        // проверяем точку в левой ВО
        size_t next_left = (U_L + 1) % L;
        if (rotate(left_hull[U_L], right_hull[U_R], left_hull[next_left]) > 0 && not_one_left && flag_left) {
            U_L = next_left;
        } else {
            flag_left = false;
        }

        // проверяем точку в правой ВО
        size_t prev_right = (U_R + R - 1) % R;
        
        if (rotate(left_hull[U_L], right_hull[U_R], right_hull[prev_right]) > 0 && not_one_right && flag_right) {
            U_R = prev_right;
        } else {
            flag_right = false;
        }
    }

    return {U_L, U_R};
}

std::pair<size_t, size_t> getLowerTangent(std::vector<Point>& left_hull, std::vector<Point>& right_hull) {
    size_t L_L = getRightmostPoint(left_hull);
    size_t L_R = getLeftmostPoint(right_hull);

    size_t L = left_hull.size();
    size_t R = right_hull.size();

    if(L == 1 && R == 1) {return {0, 0};}

    bool not_one_left = L > 1 ? true : false;
    bool not_one_right = R > 1 ? true : false;

    bool flag_left = true;
    bool flag_right = true;

    while (flag_left || flag_right) {

        // проверяем точку в левой ВО
        size_t next_left = (L_L + L - 1) % L;
        if (rotate(left_hull[L_L], right_hull[L_R], left_hull[next_left]) < 0 && not_one_left && flag_left) {
            L_L = next_left;
        } else {
            flag_left = false;
        }

        // проверяем точку в правой ВО
        size_t prev_right = (L_R + 1) % R;
        if (rotate(left_hull[L_L], right_hull[L_R], right_hull[prev_right]) < 0 && not_one_right && flag_right) {
            L_R = prev_right;
        } else {
            flag_right = false;
        }
    }

    return {L_L, L_R};
}


std::vector<std::vector<Point>> splitPoints(const std::vector<Point>& points) {
    std::vector<std::vector<Point>> result;

    // базовый случай
    if (points.size() < 4) {
        result.push_back(points);
        return result;
    }

    size_t mid = points.size() / 2;

    std::vector<Point> left(points.begin(), points.begin() + mid);
    std::vector<Point> right(points.begin() + mid, points.end());


    auto leftParts = splitPoints(left);
    auto rightParts = splitPoints(right);


    result.insert(result.end(), leftParts.begin(), leftParts.end());
    result.insert(result.end(), rightParts.begin(), rightParts.end());

    return result;
}


void MergeConvHull(std::vector<Point>& chl, std::vector<Point>& chr) {

    std::pair<size_t, size_t> upper_tangent = getUpperTangent(chl, chr);
    std::pair<size_t, size_t> lower_tangent = getLowerTangent(chl, chr);

    //left hull 

    size_t length_lpart_union = chl.size() - (upper_tangent.first - lower_tangent.first - 1);

    if (length_lpart_union == 0) {
        // вся левая ВО вошла в объединение
    } else {
        // лишь часть вошла, и длина этой части подсчитана
    }

    //right hull

    size_t length_rpart_union = upper_tangent.second - lower_tangent.second - 1;

    if(length_rpart_union == 0) {
        // вся правая ВО вошла в объединени
    } else {
        // лишь часть и длина известна
    }
}
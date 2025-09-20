#pragma once
#include <string>
#include <sstream>

class Point {
private:
    double x, y;

public:
    Point(double x_val = 0, double y_val = 0);

    double getX() const;
    double getY() const;
    void setX(double x_val);
    void setY(double y_val);

    std::string toString() const;

    // Операторы
    Point operator+(const Point& other) const;
    Point operator-(const Point& other) const;
    Point operator*(const Point& other) const; // поэлементное
    bool operator==(const Point& other) const;
};

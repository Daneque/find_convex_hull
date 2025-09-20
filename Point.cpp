#include "Point.h"
#include <cmath>

Point::Point(double x_val, double y_val) : x(x_val), y(y_val) {}

double Point::getX() const { return x; }
double Point::getY() const { return y; }
void Point::setX(double x_val) { x = x_val; }
void Point::setY(double y_val) { y = y_val; }

std::string Point::toString() const {
    std::stringstream ss;
    ss << "(" << x << ", " << y << ")";
    return ss.str();
}

Point Point::operator+(const Point& other) const {
    return Point(x + other.x, y + other.y);
}

Point Point::operator-(const Point& other) const {
    return Point(x - other.x, y - other.y);
}

Point Point::operator*(const Point& other) const {
    return Point(x * other.x, y * other.y);
}

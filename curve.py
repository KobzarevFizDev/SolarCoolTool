from scipy.interpolate import CubicSpline
from PyQt5.QtCore import Qt, QPoint

class Curve:
    def __init__(self, points):
        self.points = points
        x = self.__get_x_values()
        y = self.__get_y_values()
        self.x0 = min(x)
        self.xn = max(x)
        self.spline = CubicSpline(x,y)

    def get_value(self, t):
        x = self.__get_x_by_t(t)
        return QPoint(x, int(self.spline(x)))

    def __get_x_values(self):
        return [point.x for point in self.points]

    def __get_y_values(self):
        return [point.y for point in self.points]

    def __get_x_by_t(self, t):
        return self.x0 + (self.xn - self.x0) * t


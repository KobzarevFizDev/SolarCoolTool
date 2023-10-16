from PyQt5.QtCore import Qt, QPoint
from scipy.interpolate import CubicSpline

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.r = 10
        self.w = 1
        self.color = Qt.red

    def changePosition(self, deltaX: int, deltaY: int):
        self.x += deltaX
        self.y += deltaY

    def highlightThisPointAsSelected(self):
        self.color = Qt.blue

    def unhightlightThisPointAsSelected(self):
        self.color = Qt.red


class Curve:
    def __init__(self):
        self.numberOfSegments = 10
        self.points = list()

    @property
    def numberOfPoints(self):
        return len(self.points)

    def addPoint(self, point):
        self.points.append(point)

    def increaseNumberOfCurveSegments(self):
        self.numberOfSegments += 1

    def decreaseNumberOfCurveSegments(self):
        self.numberOfSegments -= 1

    def removePoint(self, point):
        self.points.remove(point)

    def getPoints(self):
        return self.points


    def rebuildSpline(self):
        x = self.__get_x_values()
        y = self.__get_y_values()
        self.x0 = min(x)
        self.xn = max(x)
        self.spline = CubicSpline(x,y)

    def getPoint(self, t):
        x = self.__get_x_by_t(t)
        return QPoint(x, int(self.spline(x)))

    def __get_x_values(self):
        return [point.x for point in self.points]

    def __get_y_values(self):
        return [point.y for point in self.points]

    def __get_x_by_t(self, t):
        return self.x0 + (self.xn - self.x0) * t

class CurveAreaModel:
    def __init__(self):
        self.__observers = []
        self.curve = Curve()

    @property
    def numberOfPoints(self):
        return self.curve.numberOfPoints

    def getPoints(self):
        return self.curve.getPoints()

    def getPoint(self, t):
        return self.curve.getPoint(t)

    def addPoint(self, point):
        self.curve.addPoint(point)
        if self.curve.numberOfPoints > 3:
            self.curve.rebuildSpline()
        self.notifyObservers()

    def removePoint(self, point):
        self.curve.removePoint(point)
        if self.curve.numberOfPoints > 3:
            self.curve.rebuildSpline()
        self.notifyObservers()

    def increaseNumberOfCurveSegments(self):
        self.curve.increaseNumberOfCurveSegments()
        self.notifyObservers()

    def decreaseNumberOfCurveSegments(self):
        self.curve.decreaseNumberOfCurveSegments()
        self.notifyObservers()

    def rebuildSpline(self):
        self.curve.rebuildSpline()

    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObservers(self):
        for x in self.__observers:
            x.modelIsChanged()
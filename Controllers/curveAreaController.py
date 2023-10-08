from Views.curveAreaView import CurveAreaView
from Models.curveAreaModel import Point
import math

class CurveEditorController:
    def __init__(self, model, MainAppWindow):
        self.model = model
        self.view = CurveAreaView(self, model, MainAppWindow)

    def editCurve(self, x, y):
        if self.__isClickOnAnExistingPoint(x, y):
            print("click on existing point")
            self.selectedPoint = self.__getExistingPointInArea(x, y)
        else:
            print("create new point")
            self.__createNewPoint(x, y)

    def __isClickOnAnExistingPoint(self, x, y):
        points = self.model.getPoints()

        if len(points) == 0:
            return False

        r = points[0].r
        for p in points:
            if math.sqrt( (p.x - x) * (p.x - x) + (p.y - y) * (p.y - y) ) < r:
                return True
        return False

    def __getExistingPointInArea(self, x, y):
        points = self.model.getPoints()

        if len(points) == 0:
            return False

        r = points[0].r
        for p in points:
            if math.sqrt( (p.x - x) * (p.x - x) + (p.y - y) * (p.y - y) ) < r:
                return p
        return None

    def __createNewPoint(self, x, y):
        newPoint = Point(x,y)
        self.model.addPoint(newPoint)
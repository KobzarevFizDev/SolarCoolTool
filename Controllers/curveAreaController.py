from Views.curveAreaView import CurveAreaView
from Models.curveAreaModel import Point
import math

class CurveEditorController:
    def __init__(self, model, MainAppWindow):
        self.model = model
        self.view = CurveAreaView(self, model, MainAppWindow)

    def createNewPoint(self, x, y):
        newPoint = Point(x, y)
        self.model.addPoint(newPoint)


    def mouseMove(self, x, y):
        print("mouse move")
        if not self.selectedPoint == None:
            self.model.changePoint(self.selectedPoint, x, y)

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
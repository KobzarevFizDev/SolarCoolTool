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
        return newPoint

    def deletePoint(self, point: Point):
        self.model.removePoint(point)
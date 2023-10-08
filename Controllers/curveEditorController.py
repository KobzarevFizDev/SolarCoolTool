from CustomWidgets.curveAreaWidget import CurveAreaWidget
from Models.curve import Curve
from Models.point import Point

class CurveEditorController:
    def __init__(self, curveModel:'Curve', curveView:'CurveAreaWidget'):
        self.model = curveModel
        self.view = curveView

    def addPoint(self, point):
        self.model.addPoint(point)
        self.view.drawArea(self.model.getPoints())

    def removePoint(self, point):
        self.model.removePoint(point)
        self.view.drawArea(self.model.getPoints())
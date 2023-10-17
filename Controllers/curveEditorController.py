from PyQt5.QtCore import QPoint

from Views.curveAreaView import CurveAreaView
from Models.curveAreaModel import Point

class CurveEditorController:
    def __init__(self, model, MainAppWindow):
        self.model = model
        self.view = CurveAreaView(self, model, MainAppWindow)

    def createNewPoint(self, x, y):
        newPoint = Point(x, y)
        self.model.addPoint(newPoint)
        return newPoint

    # TODO: подобрать более хорошее имя для функции
    def calculatePointsFormingBrokenLine(self):
        t_step = 1/self.model.numberOfSegments
        t_values = [t_step * i for i in range(0, self.model.numberOfSegments + 1)]
        return [self.model.getPoint(t) for t in t_values]

    def calculateTopsPointsFormingArea(self, pointsFormingBroken, widthArea):
        return [QPoint(int(p.x()), int(p.y() + widthArea / 2)) for p in pointsFormingBroken]

    #def calculateAreaSegments(self, pointsFormingBroken, widthArea):
    #    topPoints = [(int(p.x()), int(p.y() + widthArea / 2)) for p in pointsFormingBroken]
    #    bottomPoints = [(int(p.x(), int(p.y() - widthArea / 2))) for p in pointsFormingBroken]

    #    indexes = [(i, i+1) for i in range(len(pointsFormingBroken) - 1)]


    def deletePoint(self, point: Point):
        self.model.removePoint(point)

    def increaseNumberOfCurveSegments(self):
        self.model.increaseNumberOfCurveSegments()

    def decreaseNumberOfCurveSegments(self):
        self.model.decreaseNumberOfCurveSegments()
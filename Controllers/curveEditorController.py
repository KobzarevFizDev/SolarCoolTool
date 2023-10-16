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
        t_values = [0.05 * i for i in range(1, 21)]
        return [self.model.getPoint(t) for t in t_values]


    def deletePoint(self, point: Point):
        self.model.removePoint(point)

    def increaseNumberOfCurveSegments(self):
        self.model.increaseNumberOfCurveSegments()

    def decreaseNumberOfCurveSegments(self):
        self.model.decreaseNumberOfCurveSegments()
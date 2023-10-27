from PyQt5.QtCore import QPoint

from Views.curveAreaView import CurveAreaView
from Models.curveAreaModel import Point, AreaSegment


class CurveEditorController:
    def __init__(self, model, mainAppWindow):
        self.model = model
        self.view = CurveAreaView(self, model, mainAppWindow)

    def createNewPoint(self, x, y):
        newPoint = Point(x, y)
        self.model.addPoint(newPoint)
        return newPoint

    def calculatePointsFormingBrokenLine(self):
        t_step = 1/self.model.numberOfSegments
        t_values = [t_step * i for i in range(0, self.model.numberOfSegments + 1)]
        return [self.model.getPoint(t) for t in t_values]

    def calculateTopPointsFormingArea(self, pointsFormingBroken, widthArea):
        return [QPoint(int(p.x()), int(p.y() + widthArea / 2)) for p in pointsFormingBroken]

    def calculateBottomPointsFormingArea(self, pointsFormingBroken, widthArea):
        return [QPoint(int(p.x()), int(p.y() - widthArea / 2)) for p in pointsFormingBroken]

    def calculateAreaSegments(self, topsPoint, bottomPoints):
        if not len(topsPoint) == len(bottomPoints):
            Exception("number top points not equal number bottom points")

        indexes = [(i, i + 1) for i in range(len(topsPoint))]
        areaSegments = list()
        for i in range(len(indexes)-1):
            topLeftPoint = topsPoint[indexes[i][0]]
            topRightPoint = topsPoint[indexes[i][1]]
            bottomLeftPoint = bottomPoints[indexes[i][0]]
            bottomRightPoint = bottomPoints[indexes[i][1]]
            segment = AreaSegment(topRightPoint, topLeftPoint, bottomRightPoint, bottomLeftPoint)
            areaSegments.append(segment)

        return areaSegments


    def deletePoint(self, point: Point):
        self.model.removePoint(point)

    def increaseNumberOfCurveSegments(self):
        self.model.increaseNumberOfCurveSegments()

    def decreaseNumberOfCurveSegments(self):
        self.model.decreaseNumberOfCurveSegments()
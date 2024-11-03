from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem

class CurvePointWidget(QGraphicsEllipseItem):
    def __init__(self, curvePointModel,
                       curveModel,
                       curveController):
        super().__init__(0,0,20,20)
        self.isSelected = False
        self.setPos(curvePointModel.x, curvePointModel.y)
        self.setBrush(Qt.blue)
        self.curvePointModel = curvePointModel
        self.curveModel = curveModel
        self.curveController = curveController

    def mousePressEvent(self, event):
        self.isSelected = True

    def mouseReleaseEvent(self, event):
        self.isSelected = False
        self.curveModel.notifyObservers()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent'):
        self.curveController.deletePoint(self.curvePointModel)
        self.curveModel.notifyObservers()

    def mouseMoveEvent(self, event):
        if self.isSelected:
            lastCursorPosition = event.lastScenePos()
            currentCursorPosition = event.scenePos()

            origPosition = self.scenePos()

            deltaPositionX = currentCursorPosition.x() - lastCursorPosition.x()
            deltaPositionY = currentCursorPosition.y() - lastCursorPosition.y()

            currentPointPositionX = deltaPositionX + origPosition.x()
            currentPointPositionY = deltaPositionY + origPosition.y()

            self.curvePointModel.changePosition(deltaPositionX, deltaPositionY)
            self.setPos(currentPointPositionX, currentPointPositionY)
            self.curveModel.rebuildSpline()
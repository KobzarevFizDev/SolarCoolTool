from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem
from Models.curveAreaModel import Point

from Models.curveAreaModel import CurveAreaModel


class CurvePointWidget(QGraphicsEllipseItem):
    def __init__(self, curvePointModel:'Point', curveModel: 'CurveAreaModel'):
        super().__init__(0,0,20,20)
        self.isSelected = False
        print("Set pos: {0} {1}".format(curvePointModel.x,curvePointModel.y))
        self.setPos(curvePointModel.x, curvePointModel.y)
        self.setBrush(Qt.blue)
        self.curvePointModel: Point = curvePointModel
        self.curveModel: CurveAreaModel = curveModel

    def mousePressEvent(self, event):
        print("press on point")
        self.isSelected = True

    def mouseReleaseEvent(self, event):
        print("release point")
        self.isSelected = False

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
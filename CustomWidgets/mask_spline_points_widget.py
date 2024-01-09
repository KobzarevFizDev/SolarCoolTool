from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsEllipseItem
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint

from PyQt5.QtWidgets import QWidget, QGraphicsItem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.solar_editor_model import CurveModel, CurvePointModel, SolarEditorModel
    from Controllers.mask_spline_controller import MaskSplineConroller


# TODO: Стоит вынести общий класс
class ControlPointWidget(QGraphicsEllipseItem):
    def __init__(self, pointModel: QPoint, solarEditorModel):
        super().__init__(0, 0, 20, 20)
        self.setPos(pointModel)
        self.__pointModel: QPoint = pointModel
        self.__solarEditorModel = solarEditorModel
        self.setBrush(Qt.red)
        self.__isSelected: bool = False

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.red, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        top_left = QPoint(self.__pointModel.x() - 10, self.__pointModel.y() + 10)
        top_right = QPoint(self.__pointModel.x() + 10, self.__pointModel.y() + 10)
        bottom_left = QPoint(self.__pointModel.x() - 10, self.__pointModel.y() - 10)
        bottom_right = QPoint(self.__pointModel.x() + 10, self.__pointModel.y() - 10)

        painter.drawLine(top_left, top_right)
        painter.drawLine(top_right, bottom_right)
        painter.drawLine(bottom_right, bottom_left)
        painter.drawLine(bottom_left, top_left)

        painter.end()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__isSelected = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__isSelected = False

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.isSelected:
            lastCursorPosition = event.lastScenePos()
            currentCursorPosition = event.scenePos()

            origPosition = self.scenePos()

            deltaPositionX = currentCursorPosition.x() - lastCursorPosition.x()
            deltaPositionY = currentCursorPosition.y() - lastCursorPosition.y()

            currentPointPositionX = deltaPositionX + origPosition.x()
            currentPointPositionY = deltaPositionY + origPosition.y()

            self.__pointModel.setX(currentPointPositionX)
            self.__pointModel.setY(currentPointPositionY)
        self.__solarEditorModel.notifyObservers()


class AnchorPointWidget(QGraphicsEllipseItem):
    def __init__(self, pointModel: QPoint, solarEditorModel):
        super().__init__(0, 0, 10, 10)
        self.setPos(pointModel)
        self.__pointModel: QPoint = pointModel
        self.__solarEditorModel = solarEditorModel
        self.setBrush(Qt.blue)
        self.__isSelected: bool = False

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.red, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        top_left = QPoint(self.__pointModel.x() - 10, self.__pointModel.y() + 10)
        top_right = QPoint(self.__pointModel.x() + 10, self.__pointModel.y() + 10)
        bottom_left = QPoint(self.__pointModel.x() - 10, self.__pointModel.y() - 10)
        bottom_right = QPoint(self.__pointModel.x() + 10, self.__pointModel.y() - 10)

        painter.drawLine(top_left, top_right)
        painter.drawLine(top_right, bottom_right)
        painter.drawLine(bottom_right, bottom_left)
        painter.drawLine(bottom_left, top_left)

        painter.end()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__isSelected = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__isSelected = False

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.isSelected:
            lastCursorPosition = event.lastScenePos()
            currentCursorPosition = event.scenePos()

            origPosition = self.scenePos()

            deltaPositionX = currentCursorPosition.x() - lastCursorPosition.x()
            deltaPositionY = currentCursorPosition.y() - lastCursorPosition.y()

            currentPointPositionX = deltaPositionX + origPosition.x()
            currentPointPositionY = deltaPositionY + origPosition.y()

            self.__pointModel.setX(currentPointPositionX)
            self.__pointModel.setY(currentPointPositionY)
        self.__solarEditorModel.notifyObservers()

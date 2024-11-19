from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel



class BaseZoneInterestingControlPointWidget(QGraphicsEllipseItem):
    def __init__(self, point_model: QPoint, app_model):
        super().__init__(0, 0, 20, 20)
        self.setPos(point_model)
        self.__app_model = app_model
        self.__point_model: QPoint = point_model
        self.__is_selected: bool = False
    
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_selected = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_selected = False

    def mouseMoveEvent(self, event) -> None:
        if self.__is_selected:
            last_cursor_position = event.lastScenePos()
            current_cursor_position = event.scenePos()

            orig_position = self.scenePos()

            delta_position_x = current_cursor_position.x() - last_cursor_position.x()
            delta_position_y = current_cursor_position.y() - last_cursor_position.y()

            current_point_position_x = int( delta_position_x + orig_position.x() )
            current_point_position_y = int( delta_position_y + orig_position.y() )

            self.__point_model.setX(current_point_position_x)
            self.__point_model.setY(current_point_position_y)
        self.__app_model.notify_observers()


class ZoneInterestingPositionControlPointWidget(BaseZoneInterestingControlPointWidget):
    def __init__(self, point_model: QPoint, app_model):
        super().__init__(point_model, app_model)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin()
        painter.setPen(QPen(Qt.black, 2.0, Qt.DotLine))

        pos_x: int = self.__point_model.x()
        pos_y: int = self.__point_model.y() 

        a: QPoint = QPoint(pos_x, pos_y + 10)
        b: QPoint = QPoint(pos_x, pos_y - 10)
        c: QPoint = QPoint(pos_x - 10, pos_y)
        d: QPoint = QPoint(pos_x + 10, pos_y)

        painter.drawLine(a, b)
        painter.drawLine(c, d)
        painter.end()


class ZoneInterestingSizeControlPointWidget(BaseZoneInterestingControlPointWidget):
    def __init__(self, point_model: QPoint, app_model):
        super().__init__(point_model, app_model)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin()
        painter.setPen(QPen(Qt.green, 2.0, Qt.DotLine))

        pos_x: int = self.__point_model.x()
        pos_y: int = self.__point_model.y() 

        a: QPoint = QPoint(pos_x, pos_y + 10)
        b: QPoint = QPoint(pos_x, pos_y - 10)
        c: QPoint = QPoint(pos_x - 10, pos_y)
        d: QPoint = QPoint(pos_x + 10, pos_y)

        painter.drawLine(a, b)
        painter.drawLine(c, d)
        painter.end()

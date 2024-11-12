from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel


# TODO: Стоит вынести общий класс
class BezierControlPointWidget(QGraphicsEllipseItem):
    def __init__(self, point_model: QPoint, app_model):
        super().__init__(0, 0, 20, 20)
        self.setPos(point_model)
        self.__point_model: QPoint = point_model
        self.__app_model = app_model
        self.setBrush(Qt.red)
        self.__is_selected: bool = False

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.red, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        top_left = QPoint(self.__point_model.x() - 10, self.__point_model.y() + 10)
        top_right = QPoint(self.__point_model.x() + 10, self.__point_model.y() + 10)
        bottom_left = QPoint(self.__point_model.x() - 10, self.__point_model.y() - 10)
        bottom_right = QPoint(self.__point_model.x() + 10, self.__point_model.y() - 10)

        painter.drawLine(top_left, top_right)
        painter.drawLine(top_right, bottom_right)
        painter.drawLine(bottom_right, bottom_left)
        painter.drawLine(bottom_left, top_left)

        painter.end()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_selected = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_selected = False

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.__is_selected:
            last_cursor_position = event.lastScenePos()
            current_cursor_position = event.scenePos()

            orig_position = self.scenePos()

            delta_position_x = current_cursor_position.x() - last_cursor_position.x()
            delta_position_y = current_cursor_position.y() - last_cursor_position.y()

            current_point_position_x = delta_position_x + orig_position.x()
            current_point_position_y = delta_position_y + orig_position.y()

            self.__point_model.setX(current_point_position_x)
            self.__point_model.setY(current_point_position_y)
        self.__app_model.notify_observers()


class BezierAnchorPointWidget(QGraphicsEllipseItem):
    def __init__(self, point_model: QPoint, app_model):
        super().__init__(0, 0, 10, 10)
        self.setPos(point_model)
        self.__point_model: QPoint = point_model
        self.__app_model = app_model
        self.setBrush(Qt.blue)
        self.__is_selected: bool = False

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.red, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        top_left = QPoint(self.__point_model.x() - 10, self.__point_model.y() + 10)
        top_right = QPoint(self.__point_model.x() + 10, self.__point_model.y() + 10)
        bottom_left = QPoint(self.__point_model.x() - 10, self.__point_model.y() - 10)
        bottom_right = QPoint(self.__point_model.x() + 10, self.__point_model.y() - 10)

        painter.drawLine(top_left, top_right)
        painter.drawLine(top_right, bottom_right)
        painter.drawLine(bottom_right, bottom_left)
        painter.drawLine(bottom_left, top_left)

        painter.end()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_selected = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_selected = False

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.isSelected:
            last_cursor_position = event.lastScenePos()
            current_cursor_position = event.scenePos()

            orig_position = self.scenePos()

            delta_position_x = current_cursor_position.x() - last_cursor_position.x()
            delta_position_y = current_cursor_position.y() - last_cursor_position.y()

            current_point_position_x = delta_position_x + orig_position.x()
            current_point_position_y = delta_position_y + orig_position.y()

            self.__point_model.setX(current_point_position_x)
            self.__point_model.setY(current_point_position_y)
        self.__app_model.notify_observers()

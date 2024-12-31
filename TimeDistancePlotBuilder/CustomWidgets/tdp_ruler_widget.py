from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPalette, QColor, QPainter, QPen


class TdpRulerWidget(QWidget):
    def __init__(self, parent):
        super(TdpRulerWidget, self).__init__()
        self.setMinimumWidth(600)
        self.setMaximumWidth(600)
        self.setMinimumHeight(20)
        self.setMaximumHeight(20)

        self.__start_value = -1
        self.__finish_value = -1
        self.__step_value = -1

    def update_ruler(self, start_value: int, finish_value: int, step_value: int) -> None:
        self.__start_value = start_value
        self.__finish_value = finish_value
        self.__step_value = step_value

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        ruler_width: int = self.width()
        ruler_height: int = self.height()
        print(ruler_height - ruler_height // 2)

        painter.drawLine(0, ruler_height - ruler_height // 2, ruler_width, ruler_height - ruler_height // 2)

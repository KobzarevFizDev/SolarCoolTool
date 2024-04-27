from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPalette, QColor, QPainter, QPen


class TimeDistancePlotWidget(QWidget):
    def __init__(self, parent):
        super(TimeDistancePlotWidget, self).__init__()
        self.__start_border = 10
        self.__finish_border = 20
        self.__pixmap = QPixmap(600, 500)
        self.__pixmap.fill(Qt.blue)


    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        self.__draw_pixmap(painter)
        self.__draw_border(painter)
        painter.end()

    def draw_time_distance_plot(self,
                                pixmap_of_time_distance_plot: QPixmap):
        self.__pixmap = pixmap_of_time_distance_plot

    def draw_borders(self, start_border: int, finish_border: int):
        self.__start_border = start_border
        self.__finish_border = finish_border

    def __draw_pixmap(self, painter: QPainter) -> None:
        painter.drawPixmap(QPoint(), self.__pixmap)

    def __draw_border(self, painter: QPainter) -> None:
        pen = QPen(Qt.red, 1.0, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin)
        p1 = QPoint(self.__start_border, 0)
        p2 = QPoint(self.__start_border, 500)

        p3 = QPoint(self.__finish_border, 0)
        p4 = QPoint(self.__finish_border, 500)

        painter.setPen(pen)
        painter.drawLine(p1.x(), p1.y(), p2.x(), p2.y())
        painter.drawLine(p3.x(), p3.y(), p4.x(), p4.y())

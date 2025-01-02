from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPalette, QColor, QPainter, QPen


class TimeDistancePlotWidget(QWidget):
    def __init__(self, parent, length: int, height: int):
        super(TimeDistancePlotWidget, self).__init__()
        self.__start_tdp_step_pos = 10
        self.__finish_tdp_step_pos = 20
        self.__pixmap = QPixmap(length, height)
        self.__pixmap.fill(Qt.blue)


    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        self.__draw_pixmap(painter)
        self.__draw_borders_of_tdp_step(painter)
        painter.end()

    def draw_time_distance_plot(self, pixmap_of_time_distance_plot: QPixmap):
        #pixmap_of_time_distance_plot = pixmap_of_time_distance_plot.scaled(560, 560)
        self.__pixmap = pixmap_of_time_distance_plot

    def highlight_tdp_step(self, start_tdp_step_pos: int, finish_tdp_step_pos: int):
        self.__start_tdp_step_pos = start_tdp_step_pos
        self.__finish_tdp_step_pos = finish_tdp_step_pos

    def __draw_pixmap(self, painter: QPainter) -> None:
        painter.drawPixmap(QPoint(), self.__pixmap)

    def __draw_borders_of_tdp_step(self, painter: QPainter) -> None:
        pen = QPen(Qt.red, 1.0, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        
        p1 = QPoint(self.__start_tdp_step_pos, 0)
        p2 = QPoint(self.__start_tdp_step_pos, 500)

        p3 = QPoint(self.__finish_tdp_step_pos, 0)
        p4 = QPoint(self.__finish_tdp_step_pos, 500)

        print(f'draw border {self.__start_tdp_step_pos} -> {self.__finish_tdp_step_pos}')

        painter.drawLine(p1.x(), p1.y(), p2.x(), p2.y())
        painter.drawLine(p3.x(), p3.y(), p4.x(), p4.y())

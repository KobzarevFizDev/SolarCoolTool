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
        self.setMaximumHeight(30)

        self.__start = -1
        self.__finish = -1
        self.__step = -1
        self.__unit_of_measurement = ''

    def set_values(self, start: int, finish: int, step: int, unit_of_measurement: str) -> None:
        self.__start = start
        self.__finish = finish
        self.__step = step
        self.__unit_of_measurement = unit_of_measurement

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        ruler_width: int = self.width()
        ruler_height: int = self.height()

        text_width = 40
        text_height = 20
        text_offset = 25
 
        painter.drawLine(0, ruler_height, ruler_width, ruler_height)

        number_of_steps = (self.__finish - self.__start) // self.__step
        step_size_px = ruler_width // number_of_steps

        print(step_size_px)

        for i in range(self.__start, self.__finish):
            x_pos = int((i - self.__start) / self.__step * step_size_px)
            if i % self.__step == 0:
                print(x_pos)
                text = f"{i}, {self.__unit_of_measurement}"
                painter.drawText(x_pos - text_width // 2, ruler_height - text_offset, text_width, text_height, Qt.AlignRight, text)
                painter.drawLine(x_pos, ruler_height, x_pos, int( ruler_height * 0.6) )
            else:
                painter.drawLine(x_pos, ruler_height, x_pos, int( ruler_height * 0.8) )

        painter.end()


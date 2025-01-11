from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen


class TdpRulerWidget(QWidget):
    def __init__(self, parent, width: int, height: int, unit_of_measurement: str, is_horizontal: bool):
        super(TdpRulerWidget, self).__init__()
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

        self.__start = -1
        self.__finish = -1
        self.__step = -1
        self.__unit_of_measurement = unit_of_measurement
        self.__is_horizontal = is_horizontal
    

    @classmethod
    def create_time_ruler(cls, parent):
        return TdpRulerWidget(parent, width=570, height=30, unit_of_measurement='c', is_horizontal=True) 

    @classmethod
    def create_distance_along_loop_ruler(cls, parent):
        return TdpRulerWidget(parent, width=30, height=450, unit_of_measurement='Mm', is_horizontal=False)

    def set_values(self, start: int, finish: int, step: int) -> None:
        self.__start = start
        self.__finish = finish
        self.__step = step

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        
        if self.__is_horizontal:
            self.__draw_horizontal_ruler(painter)
        else:
            self.__draw_vertical_ruler(painter)
        
        painter.end()

    def __draw_horizontal_ruler(self, painter: QPainter) -> None:
        ruler_length: int = self.width()
        ruler_width: int = self.height()

        text_width = 40
        text_height = 20
        text_offset = 25

        # Основная линия линейки
        painter.drawLine(0, ruler_width, ruler_length, ruler_width)

        # Число шагов на линейке
        number_of_steps = (self.__finish - self.__start) // self.__step
        step_size_px = ruler_length / (self.__finish - self.__start)

        for i in range(self.__start, self.__finish + 1):  # +1, чтобы включить последний шаг
            x_pos = int((i - self.__start) * step_size_px)

            if i % self.__step == 0:  # Основные деления
                text = f"{i}, {self.__unit_of_measurement}"
                painter.drawText(
                    x_pos - text_width // 2, 
                    ruler_width - text_offset, 
                    text_width, 
                    text_height, 
                    Qt.AlignCenter, 
                    text
                )
                painter.drawLine(x_pos, ruler_width, x_pos, int(ruler_width * 0.6))
            elif i % (self.__step // 5) == 0:  # Промежуточные деления
                painter.drawLine(x_pos, ruler_width, x_pos, int(ruler_width * 0.8))

    # def __draw_horizontal_ruler(self, painter: QPainter) -> None:
    #     ruler_length: int = self.width()
    #     ruler_width: int = self.height()

    #     text_width = 40
    #     text_height = 20
    #     text_offset = 25
 
    #     painter.drawLine(0, ruler_width, ruler_length, ruler_width)

    #     number_of_steps = (self.__finish - self.__start) // self.__step
    #     step_size_px = ruler_length // number_of_steps

    #     for i in range(self.__start, self.__finish):
    #         x_pos = int((i - self.__start) / self.__step * step_size_px)
    #         if i % self.__step == 0:
    #             text = f"{i}, {self.__unit_of_measurement}"
    #             painter.drawText(x_pos - text_width // 2, ruler_width - text_offset, text_width, text_height, Qt.AlignRight, text)
    #             painter.drawLine(x_pos, ruler_width, x_pos, int( ruler_width * 0.6) )
    #         elif i % (self.__step // 5) == 0:
    #             painter.drawLine(x_pos, ruler_width, x_pos, int( ruler_width * 0.8) )

    def __draw_vertical_ruler(self, painter: QPainter) -> None:
        ruler_length: int = self.height()
        ruler_width: int = self.width()

        text_width = 50
        text_height = 30
        painter.drawLine(ruler_width, ruler_length, ruler_width, 0)

        number_of_steps = (self.__finish - self.__start) // self.__step
        step_size_px = ruler_length // number_of_steps

        for i in range(self.__start, self.__finish):
            y_pos = int((i - self.__start) / self.__step * step_size_px)
            if i % self.__step == 0:
                painter.save()
                painter.translate(ruler_width - text_height, y_pos + text_width // 2)
                painter.rotate(-90) 
                text = f"{i}, {self.__unit_of_measurement}"
                painter.drawText(0, 0, text_width, text_height, Qt.AlignRight, text)
                painter.restore()
                painter.drawLine(ruler_width, y_pos, int( ruler_width * 0.6), y_pos)
            elif i % (self.__step // 5) == 0:
                painter.drawLine(ruler_width, y_pos, int( ruler_width * 0.8), y_pos)


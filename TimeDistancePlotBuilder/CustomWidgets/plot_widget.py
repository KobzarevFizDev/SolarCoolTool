from PyQt5.QtWidgets import QLabel;
from PyQt5.QtGui import QPixmap, QPainter;
from PyQt5.QtCore import Qt, QPoint;



class PlotWidget(QLabel):
    def __init__(self, pixmap: QPixmap, offset: QPoint):
        super().__init__()
        self.__pixmap = pixmap
        self.__offset = offset
        self.setFixedSize(self.__pixmap.size())

    def update_plot(self, pixmap: QPixmap, offset: QPoint) -> None:
        self.__pixmap = pixmap
        self.__offset = offset
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.__offset.x(), self.__offset.y(), self.__pixmap)
        super().paintEvent(event)
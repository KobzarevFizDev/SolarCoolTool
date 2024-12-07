from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint, pyqtSignal



class PlotWidget(QLabel):
    zoom_image_signal = pyqtSignal(int, int)
    move_image_signal = pyqtSignal(int, int)
    def __init__(self, pixmap: QPixmap, offset: QPoint):
        super().__init__()
        self.__pixmap = pixmap
        self.__offset = offset
        self.setFixedSize(self.__pixmap.size())
        self.__previous_x: int = 0
        self.__previous_y: int = 0
        self.__is_moved: bool = False

    def update_plot(self, pixmap: QPixmap, offset: QPoint) -> None:
        self.__pixmap = pixmap
        self.__offset = offset
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.__offset.x(), self.__offset.y(), self.__pixmap)
        super().paintEvent(event)

    
    def mousePressEvent(self, event) -> None:
        self.__previous_x = event.x()
        self.__previous_y = event.y()
        self.__is_moved = True

    def mouseReleaseEvent(self, event) -> None:
        self.__is_moved = False

    def mouseMoveEvent(self, event) -> None:
        current_x = event.x()
        current_y = event.y()
        if self.__is_moved:
            delta_x = current_x - self.__previous_x
            delta_y = current_y - self.__previous_y
            self.move_image_signal.emit(delta_x, delta_y)
        self.__previous_x = current_x
        self.__previous_y = current_y

    def wheelEvent(self, event) -> None:
        self.zoom_image_signal.emit(event.angleDelta().x(), event.angleDelta().y())
    


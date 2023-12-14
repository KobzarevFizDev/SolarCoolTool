from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, pyqtSignal, QPoint

from IOSolarData import imagesStorage

class SolarViewerWidget(QWidget):
    wheelScrollSignal = pyqtSignal(int, int)
    mouseMoveSignal = pyqtSignal(int, int)
    def __init__(self, parent):
        super(SolarViewerWidget, self).__init__()
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.red))
        self.setPalette(palette)
        self.label = QLabel(self)

        self.__scale: int = 600
        self.__offset: QPoint = QPoint(0, 0)
        self.__previousX: int = -1
        self.__previousY: int = -1
        self.__isMoved:bool = False

        i = imagesStorage.ImagesStorage()
        self.displayImage(i.read_image_by_index(1), 600, QPoint(0,0))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        pixmapToDraw = QPixmap.fromImage(self.__currentImageToDisplay)

        painter.drawPixmap(self.__offset.x(), self.__offset.y(), pixmapToDraw)
        painter.end()

    def displayImage(self, image: QImage, scale: float, offset: QPoint) -> None:
        self.__currentImageToDisplay = image
        self.__scale = scale
        self.__offset = offset
        self.update()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__isMoved = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__isMoved = False

    def setOffsetOfSolarView(self, x: int, y:int) -> None:
        self.__offset = QPoint(x, y)
        self.update()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.wheelScrollSignal.emit(event.angleDelta().x(), event.angleDelta().y())


    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        currentX = event.x()
        currentY = event.y()
        if self.__isMoved and not self.__previousX == -1 and not self.__previousY == -1:
            deltaX = currentX - self.__previousX
            deltaY = currentY - self.__previousY
            self.mouseMoveSignal.emit(deltaX, deltaY)
        self.__previousX = currentX
        self.__previousY = currentY
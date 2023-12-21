from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint

from IOSolarData import imagesStorage


class SolarViewerWidget(QWidget):
    wheelScrollSignal = pyqtSignal(int, int)
    mouseMoveSignal = pyqtSignal(int, int)
    plotWasAllocatedSignal = pyqtSignal(QPoint, QPoint)
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
        self.__zoom: float = 1
        self.__isMoved: bool = False

        self.__firstPointOfPlotWasSelected: bool = False

        self.__topLeftPointOfSelectedPlot: QPoint = QPoint(-1, -1)
        self.__bottomRightPointOfSelectedPlot: QPoint = QPoint(-1, -1)

        i = imagesStorage.ImagesStorage()
        self.displayImage(i.read_image_by_index(1), 600,1, QPoint(0,0))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        imageToDisplay = self.__currentImageToDisplay
        imageToDisplay = imageToDisplay.scaled(self.__scale, self.__scale)
        pixmapToDraw = QPixmap.fromImage(imageToDisplay)
        painter.drawPixmap(self.__offset.x(), self.__offset.y(), pixmapToDraw)
        painter.setPen(QPen(Qt.red, 5.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(QPoint(30,30), QPoint(60,60))
        painter.end()

    def displayImage(self,
                     image: QImage,
                     scale: int,
                     zoom: float,
                     offset: QPoint) -> None:
        self.__currentImageToDisplay = image
        self.__scale = scale
        self.__zoom = zoom
        self.__offset = offset
        self.update()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__isMoved = True

    # TODO: Пользователь может выбрать точки не в том порядке
    # модель должна уметь с этим работать
    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        if not self.__firstPointOfPlotWasSelected:
            self.__topLeftPointOfSelectedPlot = QPoint(a0.x(), a0.y())
        else:
            self.__bottomRightPointOfSelectedPlot = QPoint(a0.x(), a0.y())
            self.plotWasAllocatedSignal.emit(self.__topLeftPointOfSelectedPlot, self.__bottomRightPointOfSelectedPlot)
        self.__firstPointOfPlotWasSelected = not self.__firstPointOfPlotWasSelected

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__isMoved = False

    def setOffsetOfSolarView(self, x: int, y: int) -> None:
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
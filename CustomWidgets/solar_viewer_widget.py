from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSignal

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

        i = imagesStorage.ImagesStorage()
        self.displayImage(i.read_image_by_index(1))


    def displayImage(self, image: QImage):
        self.originPixmap = QPixmap.fromImage(image)
        pixmap = self.originPixmap.scaledToWidth(600)
        self.label.setPixmap(pixmap)

    def setScaleOfSolarView(self, scale):
        pixmap = self.originPixmap.scaledToWidth(scale)
        self.label.setPixmap(pixmap)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        self.wheelScrollSignal.emit(event.angleDelta().x(), event.angleDelta().y())

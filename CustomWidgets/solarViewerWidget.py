from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout, QGridLayout, QGraphicsScene, \
    QGraphicsView, QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from IOSolarData import imagesStorage

import sunpy.visualization.colormaps as cm
import matplotlib

class SolarViewerWidget(QWidget):
    def __init__(self, parent):
        super(SolarViewerWidget, self).__init__()
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.red))
        self.setPalette(palette)
        i = imagesStorage.ImagesStorage()
        self.label = QLabel(self)
        pixmap = QPixmap.fromImage(i.read_image_by_index(1))
        pixmap = pixmap.scaledToWidth(600)
        self.label.setPixmap(pixmap)
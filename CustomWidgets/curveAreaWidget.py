from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette, QColor
from PyQt5.QtCore import Qt, QPoint, pyqtSignal


class CurveAreaWidget(QWidget):
    mousePressSignal = pyqtSignal(int, int)
    mouseReleaseSignal = pyqtSignal(int, int)
    mouseDoubleClickSignal = pyqtSignal(int, int)
    def __init__(self, parent):
        super(CurveAreaWidget, self).__init__()
        self.setMinimumSize(300, 600)
        self.setMaximumSize(300, 600)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.green))
        self.setPalette(palette)

    def mousePressEvent(self, event):
        print("press: {0} {1}".format(event.x(), event.y()))
        self.mousePressSignal.emit(event.x(), event.y())

    def mouseDoubleClickEvent(self, event):
        print("double click: {0} {1}".format(event.x(), event.y()))
        self.mouseDoubleClickSignal.emit(event.x(), event.y())


    def mouseReleaseEvent(self, event):
        print("release: {0} {1}".format(event.x(), event.y()))
        self.mouseReleaseSignal.emit(event.x(), event.y())


    def drawPoints(self, points):
        print("Draw points")
        pass

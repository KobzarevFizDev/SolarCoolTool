from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette, QColor
from PyQt5.QtCore import Qt, QPoint

class CurveAreaWidget(QWidget):
    def __init__(self, parent):
        super(CurveAreaWidget, self).__init__()
        self.setMinimumSize(300, 600)
        self.setMaximumSize(300, 600)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.green))
        self.setPalette(palette)

    def mousePressEvent(self, event):
        print("click: {0} {1}".format(event.x(), event.y()))

    def drawArea(self, points):
        print(points)
        pass

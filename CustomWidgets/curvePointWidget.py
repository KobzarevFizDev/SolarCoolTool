from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem


class CurvePointWidget(QGraphicsEllipseItem):
    def __init__(self, x, y):
        super().__init__(0,0,10,10)
        self.isSelected = False
        self.setPos(x, y)
        self.setBrush(Qt.blue)

    def mousePressEvent(self, event):
        print("press on point")
        self.isSelected = True

    def mouseReleaseEvent(self, event):
        print("release point")
        self.isSelected = False

    def mouseMoveEvent(self, event):
        print("move point")
        self.setPos(event.x(), event.y())
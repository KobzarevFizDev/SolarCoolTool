import math
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint

class Point:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r


class BezierEditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.points = list()
        self.initUI()
        self.setMouseTracking(True)
        self.selectedBezierPoint = None


    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Bezier editor')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.show()


    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        for point in self.points:
            painter.drawEllipse(QPoint(point.x, point.y), 10, 10)


    def mousePressEvent(self, event):
        if not self.isClickOnBezierPoint(QPoint(event.x(), event.y())):
            self.createBezierPoint(event.x(), event.y())
            self.update()

    def isClickOnBezierPoint(self, mouseClickPoint):
        for point in self.points:
            if ((point.x - mouseClickPoint.x()) ** 2 + (point.y - mouseClickPoint.y())**2)**0.5 < point.r * 2:
                return True
        return False

    def getSelectedBezierPoint(self, mouseClickPoint):
        for point in self.points:
            if ((point.x - mouseClickPoint.x()) ** 2 + (point.y - mouseClickPoint.y())**2)**0.5 < point.r * 2:
                return point


    def mouseReleaseEvent(self, event):
        pass


    def mouseDoubleClickEvent(self, event):
        if not self.selectedBezierPoint == None:
            self.selectedBezierPoint = None
            return

        if self.isClickOnBezierPoint(QPoint(event.x(), event.y())):
            self.selectedBezierPoint = self.getSelectedBezierPoint(QPoint(event.x(), event.y()))


    def mouseMoveEvent(self, event):
        if not self.selectedBezierPoint == None:
            self.selectedBezierPoint.x = event.x()
            self.selectedBezierPoint.y = event.y()
            self.update()

    def createBezierPoint(self, x, y):
        self.points.append(Point(x,y,10))
        self.update()

app = QApplication(sys.argv)
ex = BezierEditorWindow()
sys.exit(app.exec_())
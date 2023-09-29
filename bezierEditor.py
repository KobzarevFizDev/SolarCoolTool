import math
import select
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint

class Point:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.w = 1
        self.color = Qt.red

    def highlightThisPointAsSelected(self):
        self.color = Qt.blue

    def unhightlightThisPointAsSelected(self):
        self.color = Qt.red


class BezierEditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.points = list()
        self.initUI()
        self.setMouseTracking(True)
        self.selectedBezierPoint = None


    def initUI(self):
        layout = QGridLayout()
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Bezier editor')

    def paintEvent(self, e):
        painter = QPainter(self)
        for point in self.points:
            painter.setBrush(QBrush(point.color, Qt.SolidPattern))
            painter.drawEllipse(QPoint(point.x, point.y), 10, 10)

        painter.setBrush(QBrush(Qt.green, Qt.CrossPattern))
        ## Вынести в отдельную функцию
        if len(self.points) == 3:
            lastPoint = self.getBezierPoint(0)
            for t in [0.05 * i for i in range(1,21)]:
                print("t = {0}".format(t))
                currentPoint = self.getBezierPoint(t)
                painter.drawLine(lastPoint, currentPoint)
                lastPoint = currentPoint

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
        for i, elem in enumerate(self.points):
            point = self.points[i]
            if ((point.x - mouseClickPoint.x()) ** 2 + (point.y - mouseClickPoint.y())**2)**0.5 < point.r * 2:
                return point


    def mouseReleaseEvent(self, event):
        pass


    def wheelEvent(self, event):
        if not self.selectedBezierPoint == None:
            deltaWheel = event.angleDelta().y()
            if deltaWheel > 0:
                self.selectedBezierPoint.w += 0.05
            else:
                self.selectedBezierPoint.w -= 0.05
            print(self.selectedBezierPoint.w)


    def mouseDoubleClickEvent(self, event):
        if not self.selectedBezierPoint == None:
            self.selectedBezierPoint.unhightlightThisPointAsSelected()
            self.selectedBezierPoint = None
            self.update()
            return

        if self.isClickOnBezierPoint(QPoint(event.x(), event.y())):
            self.selectedBezierPoint = self.getSelectedBezierPoint(QPoint(event.x(), event.y()))
            self.selectedBezierPoint.highlightThisPointAsSelected()
            self.update()

    def mouseMoveEvent(self, event):
        if not self.selectedBezierPoint == None:
            self.selectedBezierPoint.x = event.x()
            self.selectedBezierPoint.y = event.y()
            self.update()

    def createBezierPoint(self, x, y):
        self.points.append(Point(x,y,10))
        self.update()

    def getBezierPoint(self, t):
        P0 = QPoint(self.points[0].x, self.points[0].y)
        P1 = QPoint(self.points[1].x, self.points[1].y)
        P2 = QPoint(self.points[2].x, self.points[2].y)

        w1 = self.points[0].w
        w2 = self.points[1].w
        w3 = self.points[2].w

        x = int((1-t)**2 * P0.x() + 2*t*(1-t)*P1.x() + t**2*P2.x())
        y = int((1-t)**2 * P0.y() + 2*t*(1-t)*P1.y() + t**2*P2.y())

        return QPoint(x,y)

app = QApplication(sys.argv)
ex = BezierEditorWindow()
ex.show()
sys.exit(app.exec_())
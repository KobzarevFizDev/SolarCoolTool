from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout, QGridLayout, QGraphicsScene, \
    QGraphicsView, QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette, QColor
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from CustomWidgets.curvePointWidget import CurvePointWidget
from Models.curveAreaModel import *


class CurveAreaWidget(QWidget):
    mousePressSignal = pyqtSignal(int, int)
    mouseReleaseSignal = pyqtSignal(int, int)
    mouseDoubleClickSignal = pyqtSignal(int, int)
    mouseMoveSignal = pyqtSignal(int, int)

    def __init__(self, parent):
        super(CurveAreaWidget, self).__init__()
        self.setMinimumSize(300, 600)
        self.setMaximumSize(300, 600)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.green))
        self.setPalette(palette)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 300, 600)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 300, 600)
        self.view.show()
        self.curvePointsWidget:list[CurvePointWidget] = list()

    def mousePressEvent(self, event):
        self.mousePressSignal.emit(event.x(), event.y())

    def mouseMoveEvent(self, event):
        print("move")
        self.mouseMoveSignal.emit(event.x(), event.y())

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickSignal.emit(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.mouseReleaseSignal.emit(event.x(), event.y())

    def drawPoint(self, newPointModel, newCurveModel, curveController):
        pointWidget = CurvePointWidget(newPointModel, newCurveModel, curveController)
        self.scene.addItem(pointWidget)
        self.curvePointsWidget.append(pointWidget)

    def drawLine(self, pointsFormingBrokenLine):
        pen = QPen(Qt.red)
        indexesOfPoints = [(i, i + 1) for i in range(len(pointsFormingBrokenLine) - 1)]
        for indexOfPoint in indexesOfPoints:
            startPoint = pointsFormingBrokenLine[indexOfPoint[0]]
            endPoint = pointsFormingBrokenLine[indexOfPoint[1]]
            self.scene.addLine(startPoint.x(), startPoint.y(), endPoint.x(), endPoint.y(), pen)
            print("drawLine: {0}, {1}".format(startPoint.x(), endPoint.x()))

    def clearAll(self):
        self.scene.clear()

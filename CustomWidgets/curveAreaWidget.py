from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout, QGridLayout, QGraphicsScene, \
    QGraphicsView
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
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 300, 600)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 300, 600)
        self.view.show()

    def mousePressEvent(self, event):
        self.mousePressSignal.emit(event.x(), event.y())

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickSignal.emit(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.mouseReleaseSignal.emit(event.x(), event.y())

    def drawArea(self, points):
        self.scene.clear()
        greenBrush = QBrush(Qt.green)
        blackPen = QPen(Qt.green)
        blackPen.setWidth(5)
        for p in points:
            print("Draw point: {0} {1}".format(p.x, p.y))
            self.scene.addEllipse(p.x, p.y, 20, 20, blackPen, greenBrush)
        self.scene.update()
        self.view.show()

    def drawSceneTest(self):
        scene = QGraphicsScene(self)
        greenBrush = QBrush(Qt.green)
        blueBrush = QBrush(Qt.blue)

        blackPen = QPen(Qt.black)
        blackPen.setWidth(5)

        scene.addEllipse(10,10,100,100,blackPen,greenBrush)
        self.view = QGraphicsView(scene, self)
        self.view.show()


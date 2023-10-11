import math
import select

from CustomWidgets.color import Color
from curve import Curve
import sys
import curve

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout, QGridLayout, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint
from CustomWidgets.curveAreaWidget import CurveAreaWidget

from Models.curveAreaModel import CurveAreaModel
from Controllers.curveAreaController import CurveEditorController


class CurveEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setGeometry(200, 200, 600, 600)
        #self.setMouseTracking(True)
        self.curveEditorModel = CurveAreaModel()
        self.curveEditorController = CurveEditorController(self.curveEditorModel, self)

    def mouseMoveEvent(self, event):
        print("move: {0}, {1}: ".format(event.x(), event.y()))
        #super().__init__()
        #self.setWindowTitle("My App")
        #self.setGeometry(200,200,600,600)
        #widget = CurveAreaWidget(self)
        #self.setCentralWidget(widget)


app = QApplication(sys.argv)
ex = CurveEditorWindow()
ex.show()
sys.exit(app.exec_())
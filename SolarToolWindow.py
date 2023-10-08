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


class CurveEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setGeometry(200,200,600,600)
        widget = CurveAreaWidget(self)
        #widget = Color('red')
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
ex = CurveEditorWindow()
ex.show()
sys.exit(app.exec_())
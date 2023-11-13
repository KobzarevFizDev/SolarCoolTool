import sys
from IOSolarData import imagesStorage

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget

from Models.curveAreaModel import CurveAreaModel
from Models.solarViewerModel import SolarViewModel

from Controllers.curveEditorController import CurveEditorController
from Controllers.solarViewerController import SolarViewerController


class CurveEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setGeometry(200, 200, 1000, 600)

        self.layout = QHBoxLayout()

        self.curveEditorModel = CurveAreaModel()
        self.solarViewerModel = SolarViewModel()

        self.curveEditorController = CurveEditorController(self.curveEditorModel, self)
        self.solarViewerController = SolarViewerController(self.solarViewerModel, self)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

    def wheelEvent(self, event):
        deltaWheel = event.angleDelta().y()
        if deltaWheel > 0:
            self.curveEditorController.increaseNumberOfCurveSegments()
        else:
            self.curveEditorController.decreaseNumberOfCurveSegments()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CurveEditorWindow()
    ex.show()
    sys.exit(app.exec_())
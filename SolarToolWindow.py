import sys

from Controllers.channelSwitchController import ChannelSwitchController
from Controllers.timeLineController import TimeLineController
from IOSolarData import imagesStorage

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QGridLayout

from Models.channelSwitchModel import ChannelSwitchModel
from Models.curveAreaModel import CurveAreaModel
from Models.solarViewerModel import SolarViewModel

from Controllers.curveEditorController import CurveEditorController
from Controllers.solarViewerController import SolarViewerController
from Models.timeLineModel import TimeLineModel

import imagesIndexer

from Models.solar_editor_model import SolarEditorModel



class CurveEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar cool tool")
        self.setGeometry(200, 200, 1200, 600)

        self.layout = QGridLayout()


        self.solarEditorModel = SolarEditorModel()

        self.curveEditorController = CurveEditorController(self.solarEditorModel.curveModel, self)
        self.solarViewerController = SolarViewerController(self.solarEditorModel.solarViewModel, self)
        self.timeLineController = TimeLineController(self.solarEditorModel.timeLineModel, self)
        self.channelSwitchController = ChannelSwitchController(self.solarEditorModel.currentChannelModel, self)

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
    indexer = imagesIndexer.ImagesIndexer("C:\\SolarImages")
    indexer.indexContents()
    app = QApplication(sys.argv)
    ex = CurveEditorWindow()
    ex.show()
    sys.exit(app.exec_())
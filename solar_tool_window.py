import sys

from Controllers.channel_switch_controller import ChannelSwitchController
from Controllers.time_line_controller import TimeLineController

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QGridLayout

from Controllers.curve_editor_controller import CurveEditorController
from Controllers.solar_viewer_controller import SolarViewerController
from Controllers.mask_spline_controller import MaskSplineConroller

from images_indexer import ImagesIndexer

from Models.solar_editor_model import SolarEditorModel



class CurveEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar cool tool")
        self.setGeometry(200, 200, 1200, 600)

        self.layout = QGridLayout()

        indexer = ImagesIndexer("C:\\SolarImages")
        indexer.indexContents()

        self.solarEditorModel = SolarEditorModel(indexer)

        self.maskSplineController = MaskSplineConroller(self.solarEditorModel, self)
        #self.curveEditorController = CurveEditorController(self.solarEditorModel, self)
        self.solarViewerController = SolarViewerController(self.solarEditorModel, self)
        self.timeLineController = TimeLineController(self.solarEditorModel, self)
        self.channelSwitchController = ChannelSwitchController(self.solarEditorModel, self)

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
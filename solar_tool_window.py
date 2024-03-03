import sys

from PyQt5 import QtCore

from Controllers.channel_switch_controller import ChannelSwitchController
from Controllers.time_line_controller import TimeLineController

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QGridLayout

from Controllers.solar_viewer_controller import SolarViewportController
from Controllers.mask_spline_controller import BezierMaskController

from Models.app_models import AppModel

class CurveEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar cool tool")
        self.setGeometry(200, 200, 1200, 600)

        self.layout = QGridLayout()
        app_model = AppModel("C:\\SolarImages")

        self.__bezier_mask_controller = BezierMaskController(app_model, self)
        self.__solar_viewer_controller = SolarViewportController(app_model, self)
        self.__time_line_controller = TimeLineController(app_model, self)
        self.__channel_switch_controller = ChannelSwitchController(app_model, self)

        """
        indexer = ImagesIndexer("C:\\SolarImages")
        indexer.indexContents()

        self.solarEditorModel = SolarEditorModel(indexer)

        self.maskExporter: MaskExporter = MaskExporter(self.solarEditorModel)
        self.resultExporter: ResultExporter = ResultExporter(self.solarEditorModel)

        self.maskSplineController = MaskSplineConroller(self.solarEditorModel, self)
        self.solarViewerController = SolarViewerController(self.solarEditorModel, self)
        self.timeLineController = TimeLineController(self.solarEditorModel, self)
        self.channelSwitchController = ChannelSwitchController(self.solarEditorModel, self)
        """
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_E:
            self.resultExporter.exportResult()
            #path = "C:\SolarImages\mask.bmp"
            #self.maskExporter.exportToBmp(path)
            #print("Exported mask to bmp. Path = {0}".format(path))

        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CurveEditorWindow()
    ex.show()
    sys.exit(app.exec_())
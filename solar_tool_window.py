import sys

from PyQt5 import QtCore

from Controllers.channel_switch_controller import ChannelSwitchController
from Controllers.time_line_controller import TimeLineController

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout

from Controllers.time_distance_plot_controller import TimeDistancePlotController
from Controllers.time_distance_plot_debug_controller import TimeDistancePlotDebugController
from Controllers.solar_viewer_controller import SolarViewportController
from Controllers.bezier_mask_controller import BezierMaskController
from Controllers.progress_controller import ProgressController
from Controllers.selected_preview_mode_controller import SelectedPreviewModeController

from Models.app_models import AppModel

class CurveEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar cool tool")
        self.setGeometry(200, 200, 1200, 600)

        self.layout = QGridLayout()

        #self.__app_model = AppModel("D:\\SolarImages",
        #                            "D:\\SolarImages")

        self.__app_model = AppModel("D:\\WangPreparated",
                                    "D:\\WangPreparated")

        self.__time_distance_controller = TimeDistancePlotController(self.__app_model, self)
        self.__time_distance_plot_debug_controller = TimeDistancePlotDebugController(self.__app_model, self)
        self.__progress_controller = ProgressController(self.__app_model, self)
        self.__selected_preview_mode_controller = SelectedPreviewModeController(self.__app_model, self)
        self.__bezier_mask_controller = BezierMaskController(self.__app_model, self)
        self.__solar_viewer_controller = SolarViewportController(self.__app_model, self)
        self.__time_line_controller = TimeLineController(self.__app_model, self)
        self.__channel_switch_controller = ChannelSwitchController(self.__app_model, self)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_E:
            self.__app_model.saver_results.save_result()
        elif event.key() == QtCore.Qt.Key_C:
            self.__app_model.saver_results.create_time_distance_plot_for_saved_data_if_possible()

        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CurveEditorWindow()
    ex.show()
    sys.exit(app.exec_())
    
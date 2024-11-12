import sys

from TimeDistancePlotBuilder.Controllers.channel_switch_controller import ChannelSwitchController
from TimeDistancePlotBuilder.Controllers.time_line_controller import TimeLineController

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout

from TimeDistancePlotBuilder.Controllers.time_distance_plot_controller import TimeDistancePlotController
from TimeDistancePlotBuilder.Controllers.time_distance_plot_debug_controller import TimeDistancePlotDebugController
from TimeDistancePlotBuilder.Controllers.solar_viewer_controller import SolarViewportController
from TimeDistancePlotBuilder.Controllers.bezier_mask_controller import BezierMaskController
from TimeDistancePlotBuilder.Controllers.progress_controller import ProgressController
from TimeDistancePlotBuilder.Controllers.selected_preview_mode_controller import SelectedPreviewModeController

from TimeDistancePlotBuilder.Models.app_models import AppModel

from TimeDistancePlotBuilder.configuration import ConfigurationApp

class CurveEditorWindow(QMainWindow):
    def __init__(self, path_to_configuration: str):
        super().__init__()
        self.setWindowTitle("Solar cool tool")
        self.setGeometry(200, 200, 1200, 600)

        self.layout = QGridLayout()

        configuration: ConfigurationApp = ConfigurationApp(path_to_configuration)

        #self.__app_model = AppModel("/home/changame/WangPreparated/A193/",
        #                            "/home/changame/WangPreparated/A193/",
        #                            193)

        self.__app_model = AppModel(configuration)

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
        event.accept()

def main():
    path_to_configuration: str = sys.argv[1]
    print(path_to_configuration)
    #app = QApplication(sys.argv)
    #ex = CurveEditorWindow()
    #ex.show()
    #sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
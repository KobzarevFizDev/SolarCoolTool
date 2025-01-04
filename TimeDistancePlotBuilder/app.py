import sys

from TimeDistancePlotBuilder.Controllers.channel_switch_controller import ChannelSwitchController
from TimeDistancePlotBuilder.Controllers.time_line_controller import TimeLineController

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtCore import QThread

from TimeDistancePlotBuilder.Controllers.time_distance_plot_controller import TimeDistancePlotController
from TimeDistancePlotBuilder.Controllers.time_distance_plot_export_controller import TimeDistancePlotExportController
from TimeDistancePlotBuilder.Controllers.solar_viewer_controller import SolarViewportController
from TimeDistancePlotBuilder.Controllers.bezier_mask_controller import BezierMaskController
from TimeDistancePlotBuilder.Controllers.select_bezier_segments_controller import SelectBezierSegmentsController
from TimeDistancePlotBuilder.Controllers.selected_preview_mode_controller import SelectedPreviewModeController

from TimeDistancePlotBuilder.Models.app_models import AppModel, NewSolarFramesStorage

from TimeDistancePlotBuilder.configuration import ConfigurationApp

from TimeDistancePlotBuilder.Popups.loading_popup import LoadingPopup


class TimeDistancePlotBuilder(QMainWindow):
    def __init__(self, path_to_configuration: str):
        super().__init__()
        self.setWindowTitle("TimeDistancePlotBuilder")
        self.setGeometry(200, 200, 1200, 600)

        self.layout = QGridLayout()

        configuration: ConfigurationApp = ConfigurationApp(path_to_configuration)

        popup = LoadingPopup(self)
        popup.show()

        self.thread1 = QThread()
        self.worker = NewSolarFramesStorage()
        self.worker.moveToThread(self.thread1)

        self.worker.progress.connect(popup.update_progress)
        self.thread1.started.connect(self.worker.process)
        self.worker.finished.connect(self.thread1.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread1.finished.connect(self.thread1.deleteLater)


        self.thread1.start()



        # self.__app_model = AppModel(configuration)

        # self.__time_distance_controller = TimeDistancePlotController(self.__app_model, self)
        # self.__time_distance_plot_debug_controller = TimeDistancePlotExportController(self.__app_model, self)
        # self.__progress_controller = SelectBezierSegmentsController(self.__app_model, self)
        # self.__selected_preview_mode_controller = SelectedPreviewModeController(self.__app_model, self)
        # self.__bezier_mask_controller = BezierMaskController(self.__app_model, self)
        # self.__solar_viewer_controller = SolarViewportController(self.__app_model, self)
        # self.__time_line_controller = TimeLineController(self.__app_model, self)
        # self.__channel_switch_controller = ChannelSwitchController(self.__app_model, self)

        # centralWidget = QWidget()
        # centralWidget.setLayout(self.layout)
        # self.setCentralWidget(centralWidget)

    def keyPressEvent(self, event):
        event.accept()

def main():
    if len(sys.argv) < 2:
        print("You need to give me path to file configuration.txt")
        exit()
    else:  
        path_to_configuration: str = sys.argv[1]
        app = QApplication(sys.argv)
        ex = TimeDistancePlotBuilder(path_to_configuration)
        # ex.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
import sys
import logging

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

from TimeDistancePlotBuilder.Models.app_models import AppModel, SolarFramesStorage

from TimeDistancePlotBuilder.configuration import ConfigurationApp

from TimeDistancePlotBuilder.Popups.popups import PopupManager


class TimeDistancePlotBuilder(QMainWindow):
    
    @property
    def popup_manager(self) -> PopupManager:
        return self.__popup_manager

    def __init__(self, path_to_configuration: str):
        super().__init__()

        self.__controllers_was_created: bool = False
        self.__popups_was_created: bool = False


        self.setWindowTitle("TimeDistancePlotBuilder")
        self.setGeometry(200, 200, 1200, 600)

        self.layout = QGridLayout()

        configuration: ConfigurationApp = ConfigurationApp(path_to_configuration)
        self.__app_model = AppModel(configuration)

        self.__popup_manager = PopupManager(self)

        self.__load_solar_frames_for_current_channel()

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)


    def __load_solar_frames_for_current_channel(self) -> None:
        current_channel: int = self.__app_model.current_channel.channel

        self.__popup_manager.loading_program_popup.show()
        
        self.__thread_load_frames = QThread()
        self.__worker = self.__app_model.solar_frames_storage
        self.__worker.moveToThread(self.__thread_load_frames)

        self.__worker.progress.connect(self.__popup_manager.loading_program_popup.update_progress)
        self.__thread_load_frames.started.connect(lambda: self.__worker.load_channel(current_channel))
        self.__worker.finished.connect(self.__thread_load_frames.quit)
        self.__worker.finished.connect(self.__worker.deleteLater)
        self.__thread_load_frames.finished.connect(self.__thread_load_frames.deleteLater)
        self.__thread_load_frames.finished.connect(self.__on_loaded_solar_frames)

        self.__thread_load_frames.start()

    def __create_controllers_if_necessary(self) -> None:
        if self.__controllers_was_created == True:
            return

        self.__time_distance_controller = TimeDistancePlotController(self.__app_model, self)
        self.__time_distance_plot_debug_controller = TimeDistancePlotExportController(self.__app_model, self)
        self.__progress_controller = SelectBezierSegmentsController(self.__app_model, self)
        self.__selected_preview_mode_controller = SelectedPreviewModeController(self.__app_model, self)
        self.__bezier_mask_controller = BezierMaskController(self.__app_model, self)
        self.__solar_viewer_controller = SolarViewportController(self.__app_model, self)
        self.__time_line_controller = TimeLineController(self.__app_model, self)
        self.__channel_switch_controller = ChannelSwitchController(self.__app_model, self)
        
        self.__controllers_was_created = True

        self.__app_model.time_line.set_finish_index_of_build_tdp_as_maximum()
        self.__app_model.notify_observers()

    def __on_loaded_solar_frames(self) -> None:
        self.__create_controllers_if_necessary()

        self.show()
        self.__popup_manager.loading_program_popup.close()

    def keyPressEvent(self, event):
        event.accept()

def main():
    if len(sys.argv) < 2:
        print("You need to give me path to configuration.txt")
        exit()
    else:  
        print("Please wait!")
        path_to_configuration: str = sys.argv[1]
        app = QApplication(sys.argv)
        ex = TimeDistancePlotBuilder(path_to_configuration)
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
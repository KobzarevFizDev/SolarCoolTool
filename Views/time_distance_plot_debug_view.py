from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout
from Models.app_models import PreviewModeEnum

if TYPE_CHECKING:
    from Models.app_models import AppModel


class TimeDistancePlotDebugView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: AppModel = model
        self.model.add_observer(self)

        self.layout = QVBoxLayout()

        self.__time_distance_window: QSlider = None
        self.__t_slider: QSlider = None

        self.__create_time_distance_window()
        self.__create_time_slider()

        parentWindow.layout.addLayout(self.layout,1,2,1,1)

        self.model_is_changed()

    def __create_time_distance_window(self):
        self.__time_distance_window = QLabel()
        self.__time_distance_window.setMinimumSize(600, 500)
        self.__time_distance_window.setMaximumSize(600, 500)
        self.layout.addWidget(self.__time_distance_window)
        pixmap = QPixmap(600, 500)
        pixmap.fill(Qt.blue)
        self.__time_distance_window.setPixmap(pixmap)

    def __create_time_slider(self):
        self.__t_slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.__t_slider)

    def model_is_changed(self):
        if self.model.selected_preview_mode.current_preview_mode == PreviewModeEnum.TEST_MODE_DISTANCE_PLOT_PREVIEW:
            self.__show_view()
        elif self.model.selected_preview_mode.current_preview_mode == PreviewModeEnum.SOLAR_PREVIEW:
            self.__hide_view()

    def __hide_view(self):
        self.__time_distance_window.hide()
        self.__t_slider.hide()

    def __show_view(self):
        self.__time_distance_window.show()
        self.__t_slider.show()
        
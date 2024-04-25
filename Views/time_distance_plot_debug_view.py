from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QPushButton, QHBoxLayout

from Models.app_models import PreviewModeEnum

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.time_distance_plot_debug_controller import TimeDistancePlotDebugController


class TimeDistancePlotDebugView:
    def __init__(self, controller, model, parentWindow):
        self.controller: TimeDistancePlotDebugController = controller
        self.model: AppModel = model
        self.model.add_observer(self)

        self.layout = QVBoxLayout()

        self.__time_distance_window: QSlider = None
        self.__t_slider: QSlider = None

        self.__create_time_distance_window()
        self.__create_time_slider()

        self.__t_slider.valueChanged.connect(self.__on_change_t)

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
        layout = QHBoxLayout()
        self.__title = QLabel("t = ")
        self.__t_slider = QSlider(Qt.Horizontal)
        self.__t_slider.setRange(0, 100)
        self.__create_timedistance_plot_button = QPushButton("Build")
        self.__create_timedistance_plot_button.clicked.connect(self.__create_time_distance_plot)
        layout.addWidget(self.__title)
        layout.addWidget(self.__t_slider)
        layout.addWidget(self.__create_timedistance_plot_button)
        self.layout.addLayout(layout)

    def model_is_changed(self):
        if self.model.selected_preview_mode.current_preview_mode == PreviewModeEnum.TEST_MODE_DISTANCE_PLOT_PREVIEW:
            self.__show_view()
            t_value = self.model.test_animated_frame.current_t
            self.__title.setText(f"t={t_value}")

        elif self.model.selected_preview_mode.current_preview_mode == PreviewModeEnum.SOLAR_PREVIEW:
            self.__hide_view()

    def set_time_distance_plot(self, pixmap_of_time_distance_plot: QPixmap):
        self.__time_distance_window.setPixmap(pixmap_of_time_distance_plot)

    def __on_change_t(self, value):
        value /= 100
        self.controller.change_t(value)

    def __hide_view(self):
        self.__time_distance_window.hide()
        self.__t_slider.hide()

    def __show_view(self):
        self.__time_distance_window.show()
        self.__t_slider.show()

    def __create_time_distance_plot(self):
        self.controller.create_debug_time_distance_plot()
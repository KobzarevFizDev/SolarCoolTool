from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QPushButton, QHBoxLayout

from CustomWidgets.time_distance_plot_widget import TimeDistancePlotWidget
from Models.app_models import PreviewModeEnum

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.time_distance_plot_debug_controller import TimeDistancePlotDebugController


class TimeDistancePlotDebugView:
    def __init__(self, controller, model, parentWindow):
        self.controller: TimeDistancePlotDebugController = controller
        self.model: AppModel = model
        self.model.add_observer(self)
        self.parentWindow = parentWindow

        self.layout = QVBoxLayout()
        self.__t_slider: QSlider = None
        self.__create_time_distance_window()
        self.__create_time_slider()
        self.__t_slider.valueChanged.connect(self.__on_change_t)

        parentWindow.layout.addLayout(self.layout, 1, 2, 1, 1)

        self.model_is_changed()

    def __create_time_distance_window(self):
        self.__time_distance_window = TimeDistancePlotWidget(None)
        self.layout.addWidget(self.__time_distance_window)

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

    def update_time_distance_plot(self,
                                  pixmap_of_time_distance_plot: QPixmap):
        pixmap = pixmap_of_time_distance_plot
        self.__time_distance_window.draw_time_distance_plot(pixmap)
        self.__time_distance_window.update()

    def update_border(self, start_border: int, finish_border: int):
        self.__time_distance_window.draw_borders(start_border, finish_border)
        self.__time_distance_window.update()

    def __on_change_t(self, value):
        value /= 100
        self.controller.change_t(value)
        self.controller.update_borders()

    def __hide_view(self):
        self.__time_distance_window.hide()
        self.__t_slider.hide()

    def __show_view(self):
        self.__time_distance_window.show()
        self.__t_slider.show()

    def __create_time_distance_plot(self):
        self.controller.create_debug_time_distance_plot()

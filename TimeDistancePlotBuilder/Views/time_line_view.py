from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QSlider, QLabel

from typing import TYPE_CHECKING
from qtrangeslider import QRangeSlider

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel
    from TimeDistancePlotBuilder.Controllers.time_line_controller import TimeLineController

class TimeLineView:
    def __init__(self, controller, model, parentWindow):
        self.controller: TimeLineController = controller
        self.model: AppModel = model
        self.model.add_observer(self)

        self.layout = QVBoxLayout()

        parentWindow.layout.addLayout(self.layout, 2, 1, 1, 3)

        self.layout.addSpacing(10)
        self.__create_time_line_slider()
        self.__create_time_distance_slider()
        self.layout.setAlignment(Qt.AlignTop)
        self.model_is_changed()

    def __create_time_line_slider(self) -> QSlider:
        self.__time_line_slider_label = QLabel("Time line:")
        self.__time_line_slider_label.setStyleSheet("font: 14pt;")
        self.layout.addWidget(self.__time_line_slider_label)
        self.__time_line_slider = QSlider(Qt.Horizontal)
        self.__time_line_slider.setMinimumWidth(1000)
        self.__time_line_slider.setMaximumWidth(1000)
        self.number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.__time_line_slider.setRange(0, self.number_images_in_channel)
        self.__time_line_slider.setMouseTracking(True)
        self.__time_line_slider.valueChanged.connect(self.controller.on_changed_value_of_time_line_slider)
        self.layout.addWidget(self.__time_line_slider)
        return self.__time_line_slider


    def __create_time_distance_slider(self) -> QSlider:
        self.__time_distance_slider_label = QLabel("Time distance plot slider:")
        self.__time_distance_slider_label.setStyleSheet("font: 14pt;")
        self.layout.addWidget(self.__time_distance_slider_label)
        self.__time_distance_plot_slider = QRangeSlider(Qt.Horizontal)
        self.number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.__time_line_slider.setRange(0, self.number_images_in_channel-1)
        self.__time_distance_plot_slider.setValue((0, self.number_images_in_channel-1))
        self.__time_distance_plot_slider.valueChanged.connect(self.controller.on_changed_value_of_time_distance_plot_slider)
        self.layout.addWidget(self.__time_distance_plot_slider)
        return self.__time_distance_plot_slider


    def model_is_changed(self):
        self.__update_time_line_slider()
        self.__update_time_distance_plot_slider()

    def __update_time_line_slider(self):
        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.__time_line_slider.setRange(0, number_images_in_channel)
        index_of_current_solar_frame: int = self.model.time_line.index_of_current_solar_frame
        self.__time_line_slider_label.setText(f"Time line. current frame = [{index_of_current_solar_frame}/{number_images_in_channel}]")

    def __update_time_distance_plot_slider(self):
        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        start_index_of_time_distance_plot: int = self.model.time_line.start_interval_of_time_distance_plot
        finish_index_of_time_distance_plot: int = self.model.time_line.finish_interval_of_time_distance_plot
        self.__time_distance_plot_slider.setRange(0, number_images_in_channel)
        self.__time_distance_slider_label.setText(f"Time distance plot slider. [{start_index_of_time_distance_plot} <-> {finish_index_of_time_distance_plot}]")

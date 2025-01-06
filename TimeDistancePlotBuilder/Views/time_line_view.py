from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSlider, QLabel

from typing import TYPE_CHECKING
from qtrangeslider import QRangeSlider

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel
    from TimeDistancePlotBuilder.Controllers.time_line_controller import TimeLineController

class TimeLineView:
    def __init__(self, controller, model, parentWindow):
        self.__controller: TimeLineController = controller
        self.__model: AppModel = model
        self.__model.add_observer(self)

        self.__layout = QVBoxLayout()

        parentWindow.layout.addLayout(self.__layout, 3, 0, 1, 3)

        self.__layout.addSpacing(10)
        self.__create_time_line_slider()
        self.__layout.setAlignment(Qt.AlignTop)

    def model_is_changed(self):
        self.__update_time_line_slider()

    def __create_time_line_slider(self) -> QSlider:
        self.__time_line_slider_label = QLabel("Time line:")
        self.__time_line_slider_label.setStyleSheet("font: 14pt;")
        self.__layout.addWidget(self.__time_line_slider_label)
        self.__time_line_slider = QSlider(Qt.Horizontal)
        self.number_images_in_channel = self.__model.current_channel.number_of_images_in_current_channel
        self.__time_line_slider.setRange(0, self.number_images_in_channel)
        self.__time_line_slider.setMouseTracking(True)
        self.__time_line_slider.valueChanged.connect(self.__controller.on_changed_value_of_time_line_slider)
        self.__layout.addWidget(self.__time_line_slider)
        return self.__time_line_slider

    def __update_time_line_slider(self) -> None:
        number_images_in_channel = self.__model.current_channel.number_of_images_in_current_channel
        self.__time_line_slider.setRange(0, number_images_in_channel)
        index_of_current_solar_frame: int = self.__model.time_line.index_of_current_solar_frame
        self.__time_line_slider_label.setText(f"Frame = [{index_of_current_solar_frame}/{number_images_in_channel - 1}]")

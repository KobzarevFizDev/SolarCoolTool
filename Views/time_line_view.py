from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QSlider, QLabel

from typing import TYPE_CHECKING
from qtrangeslider import QRangeSlider

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.time_line_controller import TimeLineController

class TimeLineView:
    def __init__(self, controller, model, parentWindow):
        self.controller: TimeLineController = controller
        self.model: AppModel = model

        self.layout = QVBoxLayout()

        self.__time_line_slider: QSlider = None
        self.__time_distance_plot_slider: QRangeSlider = None

        parentWindow.layout.addLayout(self.layout, 2, 1, 1, 3)
        self.model.add_observer(self)

        self.layout.addSpacing(10)
        self.__create_time_line_slider()
        self.__create_time_distance_slider()

        self.layout.setAlignment(Qt.AlignTop)

        self.number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel

        self.__time_line_slider.setRange(0, self.number_images_in_channel)

        self.__time_line_slider.valueChanged.connect(self.change_value_of_slider)


    def __create_time_line_slider(self) -> QSlider:
        label = QLabel("Time line:")
        label.setStyleSheet("font: 14pt;")
        self.layout.addWidget(label)
        self.__time_line_slider = QSlider(Qt.Horizontal)
        self.__time_line_slider.setMinimumWidth(1000)
        self.__time_line_slider.setMaximumWidth(1000)
        self.__time_line_slider.setMouseTracking(True)
        self.layout.addWidget(self.__time_line_slider)
        return self.__time_line_slider


    def __create_time_distance_slider(self) -> QSlider:
        label = QLabel("Time distance plot slider:")
        label.setStyleSheet("font: 14pt;")
        self.layout.addWidget(label)
        self.__time_distance_plot_slider = QRangeSlider(Qt.Horizontal)
        self.layout.addWidget(self.__time_distance_plot_slider)
        return self.__time_distance_plot_slider

    def change_value_of_slider(self, value):
        step = (self.number_images_in_channel - 1) / self.number_images_in_channel
        index_of_image = int(value*step)
        self.controller.select_image(index_of_image)

    def model_is_changed(self):
        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.__time_line_slider.setRange(0, number_images_in_channel)


        """
        self.controller: TimeLineController = controller
        self.model: AppModel = model
        self.widget = TimeLineWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 2, 1, 1, 3)
        self.model.add_observer(self)
        self.widget.selected_image_in_channel.connect(self.selected_image)

        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.widget.set_number_images_in_channel(number_images_in_channel)
        """

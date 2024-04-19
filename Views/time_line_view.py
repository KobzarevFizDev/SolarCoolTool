from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QSlider, QLabel

from CustomWidgets.time_line_widget import TimeLineWidget
from typing import TYPE_CHECKING
from qtrangeslider import QRangeSlider

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.time_line_controller import TimeLineController

class TimeLineView:
    def __init__(self, controller, model, parentWindow):
        self.controller: TimeLineController = controller
        self.model: AppModel = model
        self.widget = TimeLineWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 2, 1, 1, 3)
        self.model.add_observer(self)
        self.widget.selected_image_in_channel.connect(self.selected_image)

        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.widget.set_number_images_in_channel(number_images_in_channel)
        """
        self.controller: TimeLineController = controller
        self.model: AppModel = model
        self.layout = QVBoxLayout()
        parentWindow.layout.addLayout(self.layout, 2,1,1,3)
        self.time_line_slider: QSlider = self.__create_time_line_slider()
        self.time_distance_slider: QSlider = self.__create_time_distance_slider()
        self.layout.setAlignment(Qt.AlignTop)

        self.model.add_observer(self)
        self.time_line_slider.selected_image_in_channel.connect(self.selected_image)

        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.time_line_slider.setRange(0, number_images_in_channel)
        """
    """
    def __create_time_line_slider(self) -> QSlider:
        label = QLabel("Time line:")
        label.setStyleSheet("font: 18pt;")
        self.layout.addWidget(label)
        time_line_slider = QSlider(Qt.Horizontal)
        time_line_slider.setMinimumWidth(1000)
        time_line_slider.setMaximumWidth(1000)
        time_line_slider.setMouseTracking(True)
        self.layout.addWidget(time_line_slider)
        return time_line_slider


    def __create_time_distance_slider(self) -> QSlider:
        label = QLabel("Time distance plot slider:")
        label.setStyleSheet("font: 18pt;")
        self.layout.addWidget(label)
        range_slider = QRangeSlider(Qt.Horizontal)
        self.layout.addWidget(range_slider)
        return range_slider
    """


    def selected_image(self, indexOfImage: int) -> None:
        self.controller.select_image(indexOfImage)

    def model_is_changed(self):
        #number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        #self.time_line_slider.setRange(0, number_images_in_channel)
        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.widget.set_number_images_in_channel(number_images_in_channel)
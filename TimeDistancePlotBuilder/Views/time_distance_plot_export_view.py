from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QPushButton, QHBoxLayout

from TimeDistancePlotBuilder.CustomWidgets.time_distance_plot_widget import TimeDistancePlotWidget
from TimeDistancePlotBuilder.Models.app_models import AppStates, TimeDistancePlot

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel
    from TimeDistancePlotBuilder.Controllers.time_distance_plot_export_controller import TimeDistancePlotExportController

class TimeDistancePlotExportView:
    def __init__(self, controller, model, parent_window):
        self.controller: TimeDistancePlotExportController = controller
        self.model: AppModel = model
        self.model.add_observer(self)
        self.__parent_window = parent_window
        self.__layout = QVBoxLayout()

        self.__create_time_distance_plot_widget()
        self.__create_additional_widgets()

        self.__parent_window.layout.addLayout(self.__layout, 1, 2, 1, 1)
        self.model_is_changed()

    def model_is_changed(self):
        if self.__is_need_to_show_this_view():
            self.__show_this_view()
        else:
            self.__hide_this_view()

        self.__update_t_value()

    def update_time_distance_plot_pixmap(self, pixmap: QPixmap) -> None:
        self.__time_distance_plot_widget.draw_time_distance_plot(pixmap)
        self.__time_distance_plot_widget.update()

    def update_time_distance_plot_current_segment(self, start_border: int, finish_border: int) -> None:
        self.__time_distance_plot_widget.draw_borders(start_border, finish_border)
        self.__time_distance_plot_widget.update()

    def __update_t_value(self) -> None:
        t = self.model.test_animated_frame.current_t
        self.__label_of_t_slider.setText(f"t = {t}")

    def __is_need_to_show_this_view(self) -> bool:
        return self.model.app_state.current_state == AppStates.EXPORT_TIME_DISTANCE_PLOT_STATE

    def __create_time_distance_plot_widget(self) -> None:
        self.__time_distance_plot_widget = TimeDistancePlotWidget(self.__parent_window, length=500, height=600)
        self.__layout.addWidget(self.__time_distance_plot_widget)

    def __create_additional_widgets(self) -> None:
        l = QHBoxLayout()
        self.__label_of_t_slider = self.__create_label_of_t_slider()
        self.__t_slider = self.__create_t_slider()
        self.__bake_button = self.__create_bake_button()
        l.addWidget(self.__label_of_t_slider)
        l.addWidget(self.__t_slider)
        l.addWidget(self.__bake_button)
        self.__layout.addLayout(l)

    def __create_label_of_t_slider(self) -> QLabel:
        label = QLabel("t = 0")
        return label

    def __create_t_slider(self) -> QSlider:
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.valueChanged.connect(self.controller.change_t)
        return slider

    def __create_bake_button(self) -> QPushButton:
        bake_button = QPushButton("Bake")
        bake_button.clicked.connect(self.controller.update_debug_time_distance_plot)
        return bake_button


    def __show_this_view(self):
        self.__label_of_t_slider.show()
        self.__t_slider.show()
        self.__bake_button.show()
        self.__time_distance_plot_widget.show()

    def __hide_this_view(self):
        self.__label_of_t_slider.hide()
        self.__t_slider.hide()
        self.__bake_button.hide()
        self.__time_distance_plot_widget.hide()

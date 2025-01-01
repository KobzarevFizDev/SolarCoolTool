from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy

from TimeDistancePlotBuilder.CustomWidgets.time_distance_plot_widget import TimeDistancePlotWidget
from TimeDistancePlotBuilder.CustomWidgets.tdp_ruler_widget import TdpRulerWidget
from TimeDistancePlotBuilder.Models.app_models import AppStates

from qtrangeslider import QRangeSlider

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel
    from TimeDistancePlotBuilder.Controllers.time_distance_plot_controller import TimeDistancePlotController

class TimeDistancePlotView:
    def __init__(self, controller, model, parent_window):
        self.__controller: TimeDistancePlotController = controller
        self.__model: AppModel = model
        self.__model.add_observer(self)
        self.__parent_window = parent_window
        self.__layout = QVBoxLayout()

        self.__create_t_slider()
        self.__create_time_ruler()
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

    def __is_need_to_show_this_view(self) -> bool:
        return self.__model.app_state.current_state == AppStates.TIME_DISTANCE_PLOT_PREVIEW_STATE

    def __create_time_distance_plot_widget(self) -> None:
        container = QHBoxLayout()
        self.__time_distance_along_loop_ruler = TdpRulerWidget.create_distance_along_loop_ruler(self.__parent_window)
        self.__time_distance_along_loop_ruler.set_values(start=0, finish=600, step=100)
        self.__time_distance_plot_widget = TimeDistancePlotWidget(self.__parent_window, length=570, height=450)
        container.addWidget(self.__time_distance_along_loop_ruler, alignment=Qt.AlignTop)
        container.addWidget(self.__time_distance_plot_widget)
        self.__layout.addLayout(container)
        self.__time_distance_along_loop_ruler.update()

    def __create_t_slider(self) -> None:
        container = QHBoxLayout()
        self.__t_slider_label = QLabel('t = 0')
        self.__t_slider = QSlider(Qt.Horizontal)
        self.__t_slider.setRange(0, 100)
        self.__t_slider.valueChanged.connect(self.__controller.change_t)
        container.addWidget(self.__t_slider_label)
        container.addWidget(self.__t_slider)
        self.__layout.addLayout(container)
        # self.__layout.addWidget(self.__t_slider)

    def __create_time_ruler(self) -> None:
        container = QHBoxLayout()
        self.__tdp_time_ruler = TdpRulerWidget.create_time_ruler(self.__parent_window)  
        container.addStretch()
        container.addWidget(self.__tdp_time_ruler)
        self.__layout.addLayout(container)
        self.__tdp_time_ruler.set_values(start=10, finish=60, step=10)

    def __create_additional_widgets(self) -> None:
        build_buttons_container = QHBoxLayout()
        range_slider_container = QHBoxLayout()
        smooth_parametr_container = QHBoxLayout()
        self.__smooth_parametr_label = self.__create_smooth_parametr_label()
        self.__smooth_parametr_slider = self.__create_smooth_parametr_slider()
        smooth_parametr_container.addWidget(self.__smooth_parametr_label)
        smooth_parametr_container.addWidget(self.__smooth_parametr_slider)
        self.__label_of_range_of_tdp_build_slider: QLabel = self.__create_label_of_range_of_tdp_build_slider()
        self.__range_of_tdp_slider: QRangeSlider = self.__create_range_of_tdp_build_slider()
        self.__build_button: QPushButton = self.__create_build_button()
        self.__uniformly_build_button: QPushButton = self.__create_uniformly_build_button()
        range_slider_container.addWidget(self.__label_of_range_of_tdp_build_slider)
        range_slider_container.addWidget(self.__range_of_tdp_slider)
        build_buttons_container.addWidget(self.__build_button)
        build_buttons_container.addWidget(self.__uniformly_build_button)
        self.__layout.addLayout(smooth_parametr_container)
        self.__layout.addLayout(range_slider_container)
        self.__layout.addLayout(build_buttons_container)
    
    # def __create_time_distance_slider(self) -> QSlider:
    #     self.__time_distance_slider_label = QLabel("Time distance plot slider:")
    #     self.__time_distance_slider_label.setStyleSheet("font: 14pt;")
    #     self.layout.addWidget(self.__time_distance_slider_label)
    #     self.__time_distance_plot_slider = QRangeSlider(Qt.Horizontal)
    #     self.number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
    #     self.__time_line_slider.setRange(0, self.number_images_in_channel-1)
    #     self.__time_distance_plot_slider.setValue((0, self.number_images_in_channel-1))
    #     self.__time_distance_plot_slider.valueChanged.connect(self.controller.on_changed_value_of_time_distance_plot_slider)
    #     self.layout.addWidget(self.__time_distance_plot_slider)
    #     return self.__time_distance_plot_slider

    def __create_smooth_parametr_label(self) -> QLabel:
        return QLabel('Sigma = 0')

    def __create_smooth_parametr_slider(self) -> QSlider:
        smooth_slider = QSlider(Qt.Horizontal)
        return smooth_slider

    def __create_label_of_range_of_tdp_build_slider(self) -> QLabel:
        return QLabel('Range of tdp = [start <-> end]')

    def __create_range_of_tdp_build_slider(self) -> QRangeSlider:
        range_of_tdp_slider = QRangeSlider(Qt.Horizontal)
        return range_of_tdp_slider

    def __create_build_button(self) -> QPushButton:
        build_tdp_button = QPushButton("Build")
        build_tdp_button.clicked.connect(self.__controller.update_time_distance_plot)
        return build_tdp_button

    def __create_uniformly_build_button(self) -> QPushButton:
        uniformly_build_tdp_button = QPushButton("Uniformly build")
        uniformly_build_tdp_button.clicked.connect(self.__controller.update_time_distance_plot)
        return uniformly_build_tdp_button

    def __update_t_value(self) -> None:
        pass
        # t = self.__model.test_animated_frame.current_t
        # self.__label_of_t_slider.setText(f"t = {t}")


    def __show_this_view(self):
        # self.__label_of_t_slider.show()
        # self.__t_slider.show()
        # self.__export_button.show()
        # self.__bake_button.show()
        self.__time_distance_plot_widget.show()

    def __hide_this_view(self):
        # self.__label_of_t_slider.hide()
        # self.__t_slider.hide()
        # self.__export_button.hide()
        # self.__bake_button.hide()
        self.__time_distance_plot_widget.hide()

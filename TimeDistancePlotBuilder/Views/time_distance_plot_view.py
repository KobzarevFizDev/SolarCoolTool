from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QHBoxLayout, QPushButton

from TimeDistancePlotBuilder.CustomWidgets.time_distance_plot_widget import TimeDistancePlotWidget
from TimeDistancePlotBuilder.CustomWidgets.tdp_ruler_widget import TdpRulerWidget
from TimeDistancePlotBuilder.Models.app_models import AppStates

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
        self.__create_ruler()
        self.__create_time_distance_plot_widget()
        # self.__create_additional_widgets()

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
        self.__time_distance_plot_widget = TimeDistancePlotWidget(self.__parent_window)
        self.__layout.addWidget(self.__time_distance_plot_widget)

    def __create_t_slider(self) -> None:
        self.__t_slider = QSlider(Qt.Horizontal)
        self.__t_slider.setRange(0, 100)
        self.__t_slider.valueChanged.connect(self.__controller.change_t)
        self.__layout.addWidget(self.__t_slider)

    def __create_ruler(self) -> None:
        self.__tdp_ruler = TdpRulerWidget(self.__parent_window)
        self.__layout.addWidget(self.__tdp_ruler)
        self.__tdp_ruler.update_ruler(0, 50, 2)

    def __create_additional_widgets(self) -> None:
        l = QHBoxLayout()
        self.__label_of_t_slider = self.__create_label_of_t_slider()
        # self.__t_slider = self.__create_t_slider()
        self.__bake_button = self.__create_bake_button()
        self.__export_button = self.__create_export_button()
        l.addWidget(self.__label_of_t_slider)
        # l.addWidget(self.__t_slider)
        l.addWidget(self.__bake_button)
        l.addWidget(self.__export_button)
        self.__layout.addLayout(l)

    def __create_label_of_t_slider(self) -> QLabel:
        label = QLabel("t = 0")
        return label

    # def __create_t_slider(self) -> QSlider:
    #     slider = QSlider(Qt.Horizontal)
    #     slider.setRange(0, 100)
    #     slider.valueChanged.connect(self.controller.change_t)
    #     return slider

    def __create_bake_button(self) -> QPushButton:
        bake_button = QPushButton("Bake")
        bake_button.clicked.connect(self.__controller.update_time_distance_plot)
        return bake_button

    def __create_export_button(self) -> QPushButton:
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.__controller.export_time_distance_plot)
        return export_button

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

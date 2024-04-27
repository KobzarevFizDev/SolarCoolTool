from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QPushButton, QHBoxLayout

from CustomWidgets.time_distance_plot_widget import TimeDistancePlotWidget
from Models.app_models import PreviewModeEnum, TimeDistancePlot

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.time_distance_plot_debug_controller import TimeDistancePlotDebugController

class TimeDistancePlotDebugView:
    def __init__(self, controller, model, parent_window):
        self.controller: TimeDistancePlotDebugController = controller
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
        return self.model.selected_preview_mode.current_preview_mode == PreviewModeEnum.TEST_MODE_DISTANCE_PLOT_PREVIEW

    def __create_time_distance_plot_widget(self) -> None:
        self.__time_distance_plot_widget = TimeDistancePlotWidget(self.__parent_window)
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
        slider.valueChanged.connect(self.__on_changed_t)
        return slider

    def __create_bake_button(self) -> QPushButton:
        bake_button = QPushButton("Bake")
        bake_button.clicked.connect(self.__on_bake_button_clicked)
        return bake_button


    def __on_changed_t(self, t: int) -> None:
        t /= 100
        self.controller.change_t(t)

    def __on_bake_button_clicked(self) -> None:
        self.controller.update_debug_time_distance_plot()

    def __show_this_view(self):
        self.__label_of_t_slider.show()
        self.__t_slider.show()
        self.__bake_button.show()

    def __hide_this_view(self):
        self.__label_of_t_slider.hide()
        self.__t_slider.hide()
        self.__bake_button.hide()

"""
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


    # todo: Эта функция вызывается каждый раз при нажатии bake Это очень тупо
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

"""
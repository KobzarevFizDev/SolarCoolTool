from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QPushButton, QHBoxLayout

from CustomWidgets.time_distance_plot_widget import TimeDistancePlotWidget
from Models.app_models import PreviewModeEnum

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.time_distance_plot_controller import TimeDistancePlotController


class TimeDistancePlotView:
    def __init__(self, controller, model, parent_window):
        self.controller: TimeDistancePlotController = controller
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

    def __is_need_to_show_this_view(self) -> bool:
        return self.model.selected_preview_mode.current_preview_mode == PreviewModeEnum.DISTANCE_PLOT_PREVIEW

    def __create_time_distance_plot_widget(self) -> None:
        time_distance_plot_widget = TimeDistancePlotWidget(self.__parent_window)
        self.__layout.addWidget(time_distance_plot_widget)

    def __create_additional_widgets(self) -> None:
        l = QHBoxLayout()
        self.__label_of_t_slider = self.__create_label_of_t_slider()
        self.__t_slider = self.__create_t_slider()
        self.__bake_button = self.__create_bake_button()
        self.__export_button = self.__create_export_button()
        l.addWidget(self.__label_of_t_slider)
        l.addWidget(self.__t_slider)
        l.addWidget(self.__bake_button)
        l.addWidget(self.__export_button)
        self.__layout.addLayout(l)

    def __create_label_of_t_slider(self) -> QLabel:
        label = QLabel("t = 0")
        return label

    def __create_t_slider(self) -> QSlider:
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.valueChanged.connect(self.__on_change_t)
        return slider

    def __create_bake_button(self) -> QPushButton:
        bake_button = QPushButton("Bake")
        bake_button.clicked.connect(self.__on_bake_button_clicked)
        return bake_button

    def __create_export_button(self) -> QPushButton:
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.__on_export_button_clicked)
        return export_button

    def __on_bake_button_clicked(self) -> None:
        print("TimeDistancePlotView::on_bake_button_clicked")

    def __on_export_button_clicked(self) -> None:
        print("TimeDistancePlotView::on_export_button_clicked")

    def __on_change_t(self, t: int):
        print(f"TimeDistancePlotView::on_change_t = {t}")

    def __show_this_view(self):
        self.__label_of_t_slider.show()
        self.__t_slider.show()
        self.__export_button.show()
        self.__bake_button.show()

    def __hide_this_view(self):
        self.__label_of_t_slider.hide()
        self.__t_slider.hide()
        self.__export_button.hide()
        self.__bake_button.hide()

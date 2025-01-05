from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QPushButton, QHBoxLayout

from TimeDistancePlotBuilder.CustomWidgets.time_distance_plot_widget import TimeDistancePlotWidget
from TimeDistancePlotBuilder.CustomWidgets.tdp_matplotlib_preview_widget import TDP_MatplotlibPreviewWidget
from TimeDistancePlotBuilder.Models.app_models import AppStates, TimeDistancePlot

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel
    from TimeDistancePlotBuilder.Controllers.time_distance_plot_export_controller import TimeDistancePlotExportController
    from matplotlib.colors import Colormap

class TimeDistancePlotExportView:
    def __init__(self, controller, model, parent_window):
        self.__controller: TimeDistancePlotExportController = controller
        self.__model: AppModel = model
        self.__model.add_observer(self)
        self.__parent_window = parent_window
        self.__layout = QVBoxLayout()
        self.__create_tdp_matplotlib_preview()

        self.__parent_window.layout.addLayout(self.__layout, 1, 2, 1, 1)
        self.model_is_changed()

    def model_is_changed(self):
        if self.__is_need_to_show_this_view():
            self.__show_all_widgets_in_layout(self.__layout)
        else:
            self.__hide_all_widgets_in_layout(self.__layout)

        if self.__model.time_distance_plot.was_builded:
            self.__update_tdp_matplotlib_preview()  

    # todo: Вынести в контроллер ?
    def __is_need_to_show_this_view(self) -> bool:
        return self.__model.app_state.current_state == AppStates.EXPORT_TIME_DISTANCE_PLOT_STATE

    def __create_tdp_matplotlib_preview(self) -> None:
        placeholder_tdp: npt.NDArray = self.__model.time_distance_plot.get_placeholder(width_in_px=900, height_in_px=300)
        cmap: Colormap = self.__model.time_distance_plot.cmap
        channel: int = self.__model.current_channel.channel

        self.__tdp_matplotlib_preview = TDP_MatplotlibPreviewWidget(placeholder_tdp, channel, cmap, self.__parent_window)
        self.__tdp_matplotlib_preview.show_time_distance_plot()
        self.__layout.addWidget(self.__tdp_matplotlib_preview)

    def __update_tdp_matplotlib_preview(self) -> None:
        tdp: npt.NDArray = self.__model.time_distance_plot.tdp_array
        cmap: Colormap = self.__model.time_distance_plot.cmap
        channel: int = self.__model.current_channel.channel
        
        self.__tdp_matplotlib_preview.change_tdp(tdp)
        self.__tdp_matplotlib_preview.change_channel(channel, cmap)
        self.__tdp_matplotlib_preview.show_time_distance_plot()

    def __create_export_plot_button(self) -> None:
        pass 

    def __show_all_widgets_in_layout(self, layout) -> None:
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.show()
            elif item.layout():
                self.__show_all_widgets_in_layout(item.layout())

    def __hide_all_widgets_in_layout(self, layout) -> None:
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.hide()
            elif item.layout():
                self.__hide_all_widgets_in_layout(item.layout())


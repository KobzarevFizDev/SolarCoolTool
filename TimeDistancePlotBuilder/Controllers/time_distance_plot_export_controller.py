from typing import TYPE_CHECKING

from TimeDistancePlotBuilder.Models.app_models import AppModel
from TimeDistancePlotBuilder.Views.time_distance_plot_export_view import TimeDistancePlotExportView
from TimeDistancePlotBuilder.Popups.popups import PopupManager
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

class TimeDistancePlotExportController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view: TimeDistancePlotExportView = TimeDistancePlotExportView(self, model, mainAppWindow)
        self.__popup_manager: PopupManager = mainAppWindow.popup_manager

    def export_tdp_as_matplotlib_plot(self, widget: QWidget) -> None:
        image_for_save: QPixmap = widget.grab()
        path_to_save: str = self.__model.configuration.path_to_export_results
        self.__popup_manager.export_image_popup.activate(image_for_save, path_to_save)

        # image_for_save: QPixmap = self.__model.time_distance_plot.get_full_pixmap()
        # path_to_save: str = self.__model.configuration.path_to_export_results
        # self.__popup_manager.export_image_popup.activate(image_for_save, path_to_save)
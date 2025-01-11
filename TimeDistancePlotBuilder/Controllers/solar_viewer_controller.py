from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint

from TimeDistancePlotBuilder.Views.solar_viewer_view import SolarViewportView
from TimeDistancePlotBuilder.Models.app_models import AppModel

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Popups.popups import PopupManager
    from PyQt5.QtGui import QPixmap

class SolarViewportController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view = SolarViewportView(self, model, mainAppWindow)
        self.__popups_manager: PopupManager = mainAppWindow.popup_manager

    def increase_zoom(self, delta) -> None:
        self.__model.viewport_transform.zoom += delta
        self.__model.notify_observers()

    def decrease_zoom(self, delta) -> None:
        self.__model.viewport_transform.zoom -= delta
        self.__model.notify_observers()

    def move_solar_image(self, delta) -> None:
        self.__model.viewport_transform.offset += delta
        self.__model.notify_observers()

    def set_position_of_zone_interesting_position_anchor(self, pos_x: int, pos_y: int) -> None:
        anchor_pos = QPoint(pos_x, pos_y)
        self.__model.zone_interesting.set_position_of_position_anchor(anchor_pos)
        self.__model.notify_observers()

    def set_position_of_zone_interesting_size_anchor(self, pos_x: int, pos_y: int) -> None:
        anchor_pos = QPoint(pos_x, pos_y)
        self.__model.zone_interesting.set_position_of_size_anchor(anchor_pos)
        self.__model.notify_observers()

    def export_solar_view(self, widget):
        path_to_export: str = self.__model.configuration.path_to_export_results
        image_for_save: QPixmap = widget.grab()
        self.__popups_manager.export_image_popup.activate(image_for_save, path_to_export)

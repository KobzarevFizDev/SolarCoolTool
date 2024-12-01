from PyQt5.QtCore import QPoint

from TimeDistancePlotBuilder.Views.solar_viewer_view import SolarViewportView
from TimeDistancePlotBuilder.Models.app_models import AppModel

class SolarViewportController:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view = SolarViewportView(self, model, mainAppWindow)

    def increase_zoom(self, delta) -> None:
        self.model.viewport_transform.zoom += delta
        self.model.notify_observers()

    def decrease_zoom(self, delta) -> None:
        self.model.viewport_transform.zoom -= delta
        self.model.notify_observers()

    def move_solar_image(self, delta) -> None:
        self.model.viewport_transform.offset += delta
        self.model.notify_observers()

    def set_position_of_zone_interesting_position_anchor(self, pos_x: int, pos_y: int) -> None:
        anchor_pos = QPoint(pos_x, pos_y)
        self.model.zone_interesting.set_position_of_position_anchor(anchor_pos)
        self.model.notify_observers()

    def set_position_of_zone_interesting_size_anchor(self, pos_x: int, pos_y: int) -> None:
        anchor_pos = QPoint(pos_x, pos_y)
        self.model.zone_interesting.set_position_of_size_anchor(anchor_pos)
        self.model.notify_observers()

    




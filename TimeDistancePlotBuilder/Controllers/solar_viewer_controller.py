from PyQt5.QtCore import QPoint

from Views.solar_viewer_view import SolarViewportView
from Models.app_models import AppModel

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

    def select_plot_of_image(self,
                             top_right_point_in_view: QPoint,
                             bottom_left_point_in_view: QPoint) -> None:
        self.model.interesting_solar_region.set_top_right_in_view(top_right_point_in_view)
        self.model.interesting_solar_region.set_bottom_left_in_view(bottom_left_point_in_view)
        self.model.notify_observers()


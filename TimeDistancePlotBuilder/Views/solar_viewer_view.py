from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint

from TimeDistancePlotBuilder.CustomWidgets.solar_viewer_widget import SolarViewerWidget

from TimeDistancePlotBuilder.Models.app_models import AppStates

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel
    from TimeDistancePlotBuilder.Controllers.solar_viewer_controller import SolarViewportController

class SolarViewportView:
    def __init__(self, controller, model, parentWindow):
        self.controller: SolarViewportController = controller
        self.model: AppModel = model
        self.widget: SolarViewerWidget = SolarViewerWidget(parentWindow, model)
        parentWindow.layout.addWidget(self.widget, 1, 2, 1, 1)
        self.model.add_observer(self)
        self.widget.zoom_image_signal.connect(self.zoom)
        self.widget.move_image_signal.connect(self.move)
        self.widget.on_changed_position_of_zone_interesting_position_anchor_signal.connect(self.on_changed_position_of_zone_interesting_position_anchor)
        self.widget.on_changed_position_of_zone_interesting_size_anchor_signal.connect(self.on_changed_size_of_zone_interesting_size_anchor)


    def zoom(self, x, y):
        if y > 0:
            self.controller.increase_zoom(0.05)
        else:
            self.controller.decrease_zoom(0.05)

    def move(self, x, y):
        self.controller.move_solar_image(QPoint(x, y))

    def on_changed_position_of_zone_interesting_position_anchor(self, pos_x: int, pos_y: int) -> None:
        self.controller.set_position_of_zone_interesting_position_anchor(pos_x, pos_y)

    def on_changed_size_of_zone_interesting_size_anchor(self, pos_x: int, pos_y: int) -> None:
        self.controller.set_position_of_zone_interesting_size_anchor(pos_x, pos_y)

    def model_is_changed(self):
        if self.model.selected_preview_mode.state == AppStates.SOLAR_PREVIEW_STATE:
            self.__show_view()
            self.__handle_view()
        else:
            self.__hide_view()

    def __hide_view(self):
        self.widget.hide()

    def __show_view(self):
        self.widget.show()

    def __handle_view(self):
        solar_frame = self.model.time_line.current_solar_frame
        pixmap_of_solar_to_show = self.model.viewport_transform.get_transformed_pixmap_for_viewport(solar_frame)
        offset = self.model.viewport_transform.offset
        self.widget.update_position_of_zone_interesting_position_anchor(self.model.zone_interesting.bottom_right_in_view)
        self.widget.update_position_of_zone_interesting_size_anchor(self.model.zone_interesting.top_left_in_view)
        self.widget.set_solar_frame_to_draw(pixmap_of_solar_to_show, offset)
        self.widget.update_widget()

from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint

from CustomWidgets.solar_viewer_widget import SolarViewerWidget

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.solar_viewer_controller import SolarViewportController

class SolarViewportView:
    def __init__(self, controller, model, parentWindow):
        self.controller: SolarViewportController = controller
        self.model: AppModel = model
        self.widget: SolarViewerWidget = SolarViewerWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget,1,2,1,1)
        self.model.add_observer(self)
        self.widget.wheelScrollSignal.connect(self.zoom)
        self.widget.mouseMoveSignal.connect(self.move)
        self.widget.plotWasAllocatedSignal.connect(self.on_select_plot)
        self.controller.select_plot_of_image(QPoint(0, 600), QPoint(600, 0))

    def zoom(self, x, y):
        if y > 0:
            self.controller.increase_zoom(0.05)
        else:
            self.controller.decrease_zoom(0.05)

    def move(self, x, y):
        self.controller.move_solar_image(QPoint(x, y))

    def on_select_plot(self, top_right_point: QPoint, bottom_left_point: QPoint):
        print(top_right_point, bottom_left_point)
        self.controller.select_plot_of_image(top_right_point, bottom_left_point)

    def model_is_changed(self):
        solar_frame = self.model.time_line.current_solar_frame
        pixmap_of_solar_to_show = self.model.viewport_transform.get_transformed_pixmap_for_viewport(solar_frame)
        offset = self.model.viewport_transform.offset
        self.widget.set_solar_frame_to_draw(pixmap_of_solar_to_show, offset)
        top_left = self.model.interesting_solar_region.top_left_in_view
        bottom_right = self.model.interesting_solar_region.bottom_right_in_view
        self.widget.set_selected_zone_interesting(top_left, bottom_right)
        self.widget.update_widget()

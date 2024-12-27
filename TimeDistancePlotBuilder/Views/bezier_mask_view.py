from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap

from TimeDistancePlotBuilder.CustomWidgets.bezier_mask_widget import BezierMaskWidget
from TimeDistancePlotBuilder.Models.app_models import AppStates, TimeDistancePlot, Cubedata

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel, SolarFrame
    from TimeDistancePlotBuilder.Controllers.bezier_mask_controller import BezierMaskController

class BezierMaskView:
    def __init__(self, controller, model, parentWindow):
        self.controller: BezierMaskController = controller
        self.model: AppModel = model
        self.widget = BezierMaskWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 0, 1, 2)
        self.model.add_observer(self)
        self.widget.create_bezier_mask_tool(self.model.bezier_mask, self.model)
        self.widget.mouseWheelSignal.connect(self.onWheel)
        self.widget.exportSignal.connect(self.on_export_clicked)

    def onWheel(self, delta):
        self.controller.onWheel(delta)

    def on_export_clicked(self, widget):
        self.widget.hide_button_export_button()
        self.controller.on_export_bezier_mask(widget)
        self.widget.show_button_export_button()

    def model_is_changed(self):
        if self.model.app_state.current_state == AppStates.EXPORT_TIME_DISTANCE_PLOT_STATE:
            self.widget.show_button_export_button()
        else:
            self.widget.hide_button_export_button()

        self.__update_bezier_widget_state()

    def __update_bezier_widget_state(self):
        current_solar_frame: SolarFrame = self.model.time_line.current_solar_frame
        top_right: QPoint = self.model.zone_interesting.top_right_in_view
        bottom_left: QPoint = self.model.zone_interesting.bottom_left_in_view
        pixmap_of_interesting_solar_region = current_solar_frame.get_pixmap_of_solar_region(bottom_left, top_right)
        self.widget.update_background(pixmap_of_interesting_solar_region)
        self.widget.update_bezier_mask(self.model.bezier_mask)

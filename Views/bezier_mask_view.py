import math
from typing import TYPE_CHECKING

from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtGui import QImage, QPixmap

from CustomWidgets.curve_area_widget import BezierMaskWidget

if TYPE_CHECKING:
    from Models.app_models import AppModel, SolarFrame
    from Controllers.mask_spline_controller import BezierMaskController

class BezierMaskView:
    def __init__(self, controller, model, parentWindow):
        self.controller: BezierMaskController = controller
        self.model: AppModel = model
        self.widget = BezierMaskWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 0, 0, 1, 2)
        self.model.add_observer(self)
        self.widget.draw_mask(self.model.bezier_mask, self.model)

    def model_is_changed(self):
        current_solar_frame: SolarFrame = self.model.time_line.current_solar_frame
        top_left: QPoint = self.model.interesting_solar_region.top_left_in_view
        bottom_right: QPoint = self.model.interesting_solar_region.bottom_right_in_view
        pixmap_of_interesting_solar_region = current_solar_frame.get_pixmap_of_solar_region(top_left, bottom_right)
        self.widget.update_solar_plot(pixmap_of_interesting_solar_region)
        self.widget.update_spline(self.model.bezier_mask)

from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint

from CustomWidgets.bezier_mask_widget import BezierMaskWidget

if TYPE_CHECKING:
    from Models.app_models import AppModel, SolarFrame
    from Controllers.bezier_mask_controller import BezierMaskController

class BezierMaskView:
    def __init__(self, controller, model, parentWindow):
        self.controller: BezierMaskController = controller
        self.model: AppModel = model
        self.widget = BezierMaskWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 0, 1, 2)
        self.model.add_observer(self)
        self.widget.create_bezier_mask_tool(self.model.bezier_mask, self.model)
        self.widget.mouseWheelSignal.connect(self.onWheel)

    def onWheel(self, delta):
        self.controller.onWheel(delta)

    def model_is_changed(self):
        if self.model.is_test_mode:
            self.__handle_as_test_mode()
        else:
            self.__handle_as_normal()

    def __handle_as_test_mode(self):
        frame_as_qpixmap = self.model.test_animated_frame.current_frame_as_qpixmap
        self.widget.update_background(frame_as_qpixmap)
        self.widget.update_bezier_mask(self.model.bezier_mask)

    def __handle_as_normal(self):
        current_solar_frame: SolarFrame = self.model.time_line.current_solar_frame
        top_right: QPoint = self.model.interesting_solar_region.top_right_in_view
        bottom_left: QPoint = self.model.interesting_solar_region.bottom_left_in_view
        pixmap_of_interesting_solar_region = current_solar_frame.get_pixmap_of_solar_region(bottom_left, top_right)
        self.widget.update_background(pixmap_of_interesting_solar_region)
        self.widget.update_bezier_mask(self.model.bezier_mask)

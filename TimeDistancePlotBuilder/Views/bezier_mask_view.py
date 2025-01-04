from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap

from TimeDistancePlotBuilder.CustomWidgets.bezier_mask_widget import BezierMaskWidget
from TimeDistancePlotBuilder.Models.app_models import AppStates, TimeDistancePlot, Cubedata
from TimeDistancePlotBuilder.Models.app_models import AppModel, SolarFrame

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Controllers.bezier_mask_controller import BezierMaskController

class BezierMaskView:
    def __init__(self, controller, model, parentWindow):
        self.__controller: BezierMaskController = controller
        self.__model: AppModel = model
        self.__widget = BezierMaskWidget(parentWindow)
        parentWindow.layout.addWidget(self.__widget, 1, 0, 1, 2)
        self.__model.add_observer(self)
        self.__widget.create_bezier_mask_tool(self.__model.bezier_mask, self.__model)
        self.__widget.mouse_wheel_signal.connect(self.onWheel)
        self.__widget.export_signal.connect(self.on_export_clicked)

    # todo: убрать лишние обработчики 
    def onWheel(self, delta):
        self.__controller.onWheel(delta)

    def on_export_clicked(self, widget):
        self.__widget.hide_export_button()
        self.__controller.export_bezier_mask(widget)
        self.__widget.show_export_button()

    def model_is_changed(self):
        self.__update_bezier()
        self.__update_pixmap()

    def __update_bezier(self) -> None:
        self.__widget.update_bezier_mask(self.__model.bezier_mask, self.__model)

    def __update_pixmap(self) -> None:
        current_solar_frame: SolarFrame = self.__get_solar_frame_for_render()
        top_right: QPoint = self.__model.zone_interesting.top_right_in_view
        bottom_left: QPoint = self.__model.zone_interesting.bottom_left_in_view
        pixmap_of_interesting_solar_region = current_solar_frame.get_pixmap_of_solar_region(bottom_left, top_right)
        self.__widget.update_background(pixmap_of_interesting_solar_region)

    def __get_solar_frame_for_render(self) -> SolarFrame:
        if self.__model.app_state.current_state == AppStates.TIME_DISTANCE_PLOT_PREVIEW_STATE:
            return self.__model.time_line.solar_frame_by_current_tdp_step
        else:
            return self.__model.time_line.current_solar_frame

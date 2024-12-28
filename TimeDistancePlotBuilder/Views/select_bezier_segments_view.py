from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from TimeDistancePlotBuilder.CustomWidgets.select_bezier_segments_widget import SelectBezierSegmentsWidget

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel, SolarFrame
    from TimeDistancePlotBuilder.Controllers.select_bezier_segments_controller import SelectBezierSegmentsController

class SelectBezierSegmentsView:
    def __init__(self, controller, model, parentWindow):
        self.__controller: SelectBezierSegmentsController = controller
        self.__model: AppModel = model
        self.__model.add_observer(self)
        self.__widget = SelectBezierSegmentsWidget(parentWindow)
        self.__widget.state_of_bezier_segment_was_changed.connect(self.state_of_segment_was_changed)
        parentWindow.layout.addWidget(self.__widget, 0, 0, 1, 2)

    def state_of_segment_was_changed(self, index: int) -> None:
        self.__controller.toggle_state_of_bezier_segment(index)

    def model_is_changed(self):
        for index_of_button in range(self.__model.selected_bezier_segments.number_of_bizer_segments):
            status_of_button: bool = self.__model.selected_bezier_segments.status_of_segment(index_of_button)
            if status_of_button:
                self.__widget.set_segment_as_selected(index_of_button)  
            else:
                self.__widget.set_segment_as_unselected(index_of_button)

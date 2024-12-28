from TimeDistancePlotBuilder.Views.select_bezier_segments_view import SelectBezierSegmentsView
from TimeDistancePlotBuilder.Models.app_models import AppModel

class SelectBezierSegmentsController:
    def __init__(self, model, mainAppWindows):
        self.__model: AppModel = model
        self.__view = SelectBezierSegmentsView(self, model, mainAppWindows)


    def toggle_state_of_bezier_segment(self, index: int) -> None:
        previous_state: bool = self.__model.selected_bezier_segments.status_of_segment(index)
        new_state = not previous_state
        if new_state:
            self.__model.selected_bezier_segments.set_segment_as_selected(index)
        else:
            self.__model.selected_bezier_segments.set_segment_as_unselected(index)

        self.__model.notify_observers()



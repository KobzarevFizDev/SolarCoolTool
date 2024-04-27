from Models.app_models import AppModel, TimeDistancePlot
from Views.time_distance_plot_debug_view import TimeDistancePlotDebugView
class TimeDistancePlotDebugController:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view: TimeDistancePlotDebugView = TimeDistancePlotDebugView(self, model, mainAppWindow)
        self.__time_distance_plot = None
        self.create_debug_time_distance_plot()

    def change_t(self, t: float):
        if t > 1 or t < 0:
            raise Exception("TimeDistancePlotDebugController::change_t() not correct value of t")

        self.model.test_animated_frame.current_t = t
        self.model.notify_observers()

    def create_debug_time_distance_plot(self):
        bezier_mask = self.model.bezier_mask
        self.__time_distance_plot = TimeDistancePlot.create_debug_distance_plot(bezier_mask)
        pixmap = self.__time_distance_plot.get_time_distance_plot_as_qpixmap_in_grayscale()
        self.view.update_time_distance_plot(pixmap)
        self.model.notify_observers()

    def update_borders(self):
        t = self.model.test_animated_frame.current_t
        start_border, finish_border = self.__time_distance_plot.get_border_of_time_distance_slice(t)
        self.view.update_border(start_border, finish_border)
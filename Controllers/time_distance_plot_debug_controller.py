from Models.app_models import AppModel, TimeDistancePlot
from Views.time_distance_plot_debug_view import TimeDistancePlotDebugView
class TimeDistancePlotDebugController:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view = TimeDistancePlotDebugView(self, model, mainAppWindow)

    def change_t(self, t: float):
        if t > 1 or t < 0:
            raise Exception("TimeDistancePlotDebugController::change_t() not correct value of t")

        self.model.test_animated_frame.current_t = t
        self.model.notify_observers()

    def create_debug_time_distance_plot(self):
        bezier_mask = self.model.bezier_mask
        plot = TimeDistancePlot.createDebugDistancePlot(bezier_mask)

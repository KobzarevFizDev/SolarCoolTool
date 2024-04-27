from Models.app_models import AppModel, TimeDistancePlot
from Views.time_distance_plot_view import TimeDistancePlotView

class TimeDistancePlotController:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view: TimeDistancePlotView = TimeDistancePlotView(self, model, mainAppWindow)

    def create_time_distance_plot(self):
        pass
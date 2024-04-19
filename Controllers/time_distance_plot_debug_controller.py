from Views.time_distance_plot_debug_view import TimeDistancePlotDebugView
class TimeDistancePlotDebugController:
    def __init__(self, model, mainAppWindow):
        self.model = model
        self.view = TimeDistancePlotDebugView(self, model, mainAppWindow)

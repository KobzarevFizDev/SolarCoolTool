from TimeDistancePlotBuilder.Models.app_models import AppModel, TimeDistancePlot
from TimeDistancePlotBuilder.Views.time_distance_plot_export_view import TimeDistancePlotExportView


class TimeDistancePlotExportController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view: TimeDistancePlotExportView = TimeDistancePlotExportView(self, model, mainAppWindow)


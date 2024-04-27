from typing import TYPE_CHECKING

from Models.app_models import AppModel, TimeDistancePlot
from Views.time_distance_plot_view import TimeDistancePlotView

if TYPE_CHECKING:
    from Models.app_models import Cubedata

class TimeDistancePlotController:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view: TimeDistancePlotView = TimeDistancePlotView(self, model, mainAppWindow)
        self.__create_time_distance_plot()

    def update_time_distance_plot(self) -> None:
        pass

    def __create_time_distance_plot(self) -> TimeDistancePlot:
        bezier_mask = self.model.bezier_mask
        start_index: int = self.model.time_line.start_interval_of_time_distance_plot
        finish_index: int = self.model.time_line.finish_interval_of_time_distance_plot
        cubedata: Cubedata = self.model.solar_frames_storage.get_cubedata_by_interval(start_index, finish_index)
        time_distance_plot: TimeDistancePlot = TimeDistancePlot.create_distance_plot_from_real_data(cubedata)

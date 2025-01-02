from TimeDistancePlotBuilder.Views.time_line_view import TimeLineView
from TimeDistancePlotBuilder.Models.app_models import AppModel

class TimeLineController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view = TimeLineView(self, model, mainAppWindow)
        self.__model.time_line.index_of_current_solar_frame = 0

    def on_changed_value_of_time_line_slider(self, value) -> None:
        number_images_in_channel = self.__model.current_channel.number_of_images_in_current_channel
        step = (number_images_in_channel - 1) / number_images_in_channel
        index_of_image = int(value*step)
        self.__model.time_line.index_of_current_solar_frame = index_of_image
        self.__model.notify_observers()

    def on_changed_value_of_time_distance_plot_slider(self, value) -> None:
        self.__model.time_line.start_frame_to_build_tdp = value[0]
        self.__model.time_line.finish_interval_of_time_distance_plot = value[1]
        self.__model.notify_observers()

    def select_image(self, index_of_image: int) -> None:
        self.__model.time_line.index_of_current_solar_frame = index_of_image
        self.__model.notify_observers()
        
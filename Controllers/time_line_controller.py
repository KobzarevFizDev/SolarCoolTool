from Views.time_line_view import TimeLineView
from Models.app_models import AppModel

class TimeLineController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view = TimeLineView(self, model, mainAppWindow)
        self.__model.time_line.index_of_current_solar_frame = 0

    def select_image(self, index_of_image: int) -> None:
        self.__model.time_line.index_of_current_solar_frame = index_of_image
        self.__model.notify_observers()
        
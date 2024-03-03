from Views.time_line_view import TimeLineView
from Models.app_models import AppModel

class TimeLineController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view = TimeLineView(self, model, mainAppWindow)

    def select_image(self, indexOfImage: int) -> None:
        self.__model.time_line.index_of_current_solar_frame = indexOfImage
        self.__model.notify_observers()
        
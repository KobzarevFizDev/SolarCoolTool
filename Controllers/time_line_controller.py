from Views.time_line_view import TimeLineView
from Models.solar_editor_model import SolarEditorModel

class TimeLineController:
    def __init__(self, model, mainAppWindow):
        self.__model: SolarEditorModel = model
        self.__view = TimeLineView(self, model, mainAppWindow)

    def selectImage(self, indexOfImage: int) -> None:
        self.__model.timeLineModel.setIndexImage(indexOfImage)
        self.__model.notifyObservers()
        
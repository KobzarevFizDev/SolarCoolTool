from Views.time_line_view import TimeLineView
from Models.solar_editor_model import SolarEditorModel

class TimeLineController:
    def __init__(self, model, mainAppWindow):
        self.model: SolarEditorModel = model
        self.view = TimeLineView(self, model, mainAppWindow)
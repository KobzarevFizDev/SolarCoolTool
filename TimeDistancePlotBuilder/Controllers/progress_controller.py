from Views.progress_view import ProgressView
from Models.app_models import AppModel

class ProgressController:
    def __init__(self, model, mainAppWindows):
        self.model = model
        self.view = ProgressView(self, model, mainAppWindows)

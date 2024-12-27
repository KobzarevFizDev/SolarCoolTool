from PyQt5.QtCore import QPoint

from TimeDistancePlotBuilder.Views.current_app_state_view import CurrentAppStateView
from TimeDistancePlotBuilder.Models.app_models import AppModel

class SelectedPreviewModeController:
    def __init__(self, model, mainAppWindow):
        self.model = model
        self.view = CurrentAppStateView(self, model, mainAppWindow)

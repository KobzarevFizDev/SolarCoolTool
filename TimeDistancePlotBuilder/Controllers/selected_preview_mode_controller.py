from PyQt5.QtCore import QPoint

from TimeDistancePlotBuilder.Views.selected_preview_mode_view import SelectedPreviewModeView
from TimeDistancePlotBuilder.Models.app_models import AppModel

class SelectedPreviewModeController:
    def __init__(self, model, mainAppWindow):
        self.model = model
        self.view = SelectedPreviewModeView(self, model, mainAppWindow)

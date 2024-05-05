from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QProgressBar

if TYPE_CHECKING:
    from Models.app_models import AppModel, SolarFrame
    from Controllers.bezier_mask_controller import BezierMaskController

class ProgressView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: AppModel = model
        self.model.add_observer(self)
        self.widget = QProgressBar()
        parentWindow.layout.addWidget(self.widget, 0, 0, 1, 2)

    def model_is_changed(self):
        pass

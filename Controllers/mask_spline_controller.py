from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint

from Views.bezier_mask_view import BezierMaskView

if TYPE_CHECKING:
    from Models.app_models import AppModel


class BezierMaskController:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view = BezierMaskView(self, model, mainAppWindow)

    def increase_number_of_segments(self):
        self.model.bezier_mask.increase_number_of_segments()
        self.model.notify_observers()

    def decrease_number_of_segments(self):
        self.model.bezier_mask.decrease_number_of_segments()
        self.model.notify_observers()

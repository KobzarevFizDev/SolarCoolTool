from typing import TYPE_CHECKING

from Views.bezier_mask_view import BezierMaskView

if TYPE_CHECKING:
    from Models.app_models import AppModel


class BezierMaskControllerTestMode:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view = BezierMaskView(self, model, mainAppWindow)

    def increase_number_of_segments(self):
        print("BezierMaskControllerTestMode::Not implemented")

    def decrease_number_of_segments(self):
        print("BezierMaskControllerTestMode::Not implemented")
from typing import TYPE_CHECKING

from Views.bezier_mask_view import BezierMaskView

if TYPE_CHECKING:
    from Models.app_models import AppModel


class BezierMaskController:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view = BezierMaskView(self, model, mainAppWindow)

    def onWheel(self, delta):
        self.__handle_test_mode(delta)

    def __handle_normal_mode(self, delta):
        if delta > 0:
            self.__increase_number_of_segments()
        else:
            self.__decrease_number_of_segments()

    def __handle_test_mode(self, delta):
        delta = -delta/8000
        self.model.test_animated_frame.animate_frame(delta)
        self.model.notify_observers()

    def __increase_number_of_segments(self):
        self.model.bezier_mask.increase_number_of_segments()
        self.model.notify_observers()

    def __decrease_number_of_segments(self):
        self.model.bezier_mask.decrease_number_of_segments()
        self.model.notify_observers()

    def __change_animated_frame(self):
        pass

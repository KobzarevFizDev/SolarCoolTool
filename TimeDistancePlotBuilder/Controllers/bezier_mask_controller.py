from typing import TYPE_CHECKING

from TimeDistancePlotBuilder.Views.bezier_mask_view import BezierMaskView
from TimeDistancePlotBuilder.Models.app_models import AppModel

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Popups.popups import PopupManager
    from PyQt5.QtGui import QPixmap


class BezierMaskController:
    def __init__(self, model: AppModel , mainAppWindow):
        self.__model: AppModel = model
        self.__view = BezierMaskView(self, model, mainAppWindow)
        self.__popups_manager: PopupManager = mainAppWindow.popup_manager

    def onWheel(self, delta):
        self.__handle_test_mode(delta)

    def export_bezier_mask(self, widget):
        image_for_save: QPixmap = widget.grab()
        self.__popups_manager.export_image_popup.activate(image_for_save, self.__model.configuration.path_to_export_results)

    def __handle_normal_mode(self, delta):
        if delta > 0:
            self.__increase_number_of_segments()
        else:
            self.__decrease_number_of_segments()

    def __handle_test_mode(self, delta):
        pass
        #delta = -delta/8000
        #self.model.test_animated_frame.animate_frame(delta)
        #self.model.notify_observers()

    def __increase_number_of_segments(self):
        self.__model.bezier_mask.increase_number_of_segments()
        self.__model.notify_observers()

    def __decrease_number_of_segments(self):
        self.__model.bezier_mask.decrease_number_of_segments()
        self.__model.notify_observers()

    def __change_animated_frame(self):
        pass

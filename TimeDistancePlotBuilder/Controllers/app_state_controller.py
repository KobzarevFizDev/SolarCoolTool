from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint


from TimeDistancePlotBuilder.Views.current_app_state_view import CurrentAppStateView
from TimeDistancePlotBuilder.Models.app_models import AppModel

class AppStateController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view = CurrentAppStateView(self, model, mainAppWindow)

    
    def select_solar_preview_state(self):
        self.__model.app_state.set_solar_preview_mode_state()
        self.__model.notify_observers()

    def select_build_tdp_state(self):
        self.__model.app_state.set_build_tdp_state()
        self.__model.notify_observers()

    def select_plot_state(self):
        self.__model.app_state.set_preview_plot_state()
        self.__model.notify_observers()
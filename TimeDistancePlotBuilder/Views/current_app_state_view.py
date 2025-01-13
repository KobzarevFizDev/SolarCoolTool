from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from TimeDistancePlotBuilder.Models.app_models import AppStates

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import AppModel

class CurrentAppStateView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: AppModel = model
        self.model.add_observer(self)
        self.layout = QHBoxLayout()

        parentWindow.layout.addLayout(self.layout, 0, 2, 1, 2)

        self.__solar_preview_button = self.__create_solar_preview_button()
        self.__distance_plot_button = self.__create_distance_plot_preview_button()
        self.__distance_plot_debug_button = self.__create_export_data_button()

    def model_is_changed(self):
        current_state = self.model.app_state.current_state
        self.__show_current_selected_state(current_state)

    def __show_current_selected_state(self, current_state: AppStates):
        buttons = {AppStates.SOLAR_PREVIEW_STATE : self.__solar_preview_button,
                  AppStates.TIME_DISTANCE_PLOT_PREVIEW_STATE : self.__distance_plot_button,
                  AppStates.EXPORT_TIME_DISTANCE_PLOT_STATE : self.__distance_plot_debug_button}
        
        for unselected_button in buttons.values():
            unselected_button.setStyleSheet("background-color: gray; color: white;")
        selected_button = buttons[current_state]
        selected_button.setStyleSheet("background-color: green; color: white;")

    def __create_solar_preview_button(self) -> QPushButton:
        button = QPushButton("SOLAR PREVIEW")
        button.clicked.connect(self.__on_selected_solar_preview_state)
        self.layout.addWidget(button)
        return button

    def __create_distance_plot_preview_button(self) -> QPushButton:
        button = QPushButton("DISTANCE PLOT")
        button.clicked.connect(self.__on_selected_distance_plot_state)
        self.layout.addWidget(button)
        return button

    def __create_export_data_button(self) -> QPushButton:
        button = QPushButton("EXPORT")
        button.clicked.connect(self.__on_selected_distance_plot_debug_state)
        self.layout.addWidget(button)
        return button

    def __on_selected_solar_preview_state(self):
        self.model.app_state.set_solar_preview_mode_state()
        self.model.notify_observers()

    def __on_selected_distance_plot_state(self):
        self.model.app_state.set_time_distance_mode_state()
        self.model.notify_observers()

    def __on_selected_distance_plot_debug_state(self):
        self.model.app_state.set_time_distance_plot_export_state()
        self.model.notify_observers()

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from TimeDistancePlotBuilder.Models.app_models import AppStates

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Controllers.app_state_controller import AppStateController
    from TimeDistancePlotBuilder.Models.app_models import AppModel

class CurrentAppStateView:
    def __init__(self, controller, model, parentWindow):
        self.__controller: AppStateController = controller
        self.__model: AppModel = model
        self.__model.add_observer(self)
        self.__layout = QHBoxLayout()

        parentWindow.layout.addLayout(self.__layout, 0, 2, 1, 2)

        self.__solar_preview_button = self.__create_solar_preview_button()
        self.__tdp_build_button = self.__create_tdp_build_button()
        self.__plot_button = self.__create_plot_button()
        self.__publish_button = self.__create_publish_button()

    def model_is_changed(self):
        current_state = self.__model.app_state.current_state
        self.__show_current_selected_state(current_state)

    def __show_current_selected_state(self, current_state: AppStates):
        buttons = {AppStates.SOLAR_PREVIEW_STATE : self.__solar_preview_button,
                  AppStates.BUILD_TDP_STATE : self.__tdp_build_button,
                  AppStates.PREVIEW_PLOT_STATE : self.__plot_button,
                  AppStates.PUBLISH_TDP_STATE : self.__publish_button}
        
        for unselected_button in buttons.values():
            unselected_button.setStyleSheet("background-color: gray; color: white;")
        selected_button = buttons[current_state]
        selected_button.setStyleSheet("background-color: green; color: white;")

    def __create_solar_preview_button(self) -> QPushButton:
        button = QPushButton("SOLAR")
        button.clicked.connect(self.__controller.set_solar_preview_state)
        self.__layout.addWidget(button)
        return button

    def __create_tdp_build_button(self) -> QPushButton:
        button = QPushButton("BUILD TDP")
        button.clicked.connect(self.__controller.set_build_tdp_state)
        self.__layout.addWidget(button)
        return button

    def __create_plot_button(self) -> QPushButton:
        button = QPushButton("PLOT")
        button.clicked.connect(self.__controller.set_plot_state)
        self.__layout.addWidget(button)
        return button
    
    def __create_publish_button(self) -> QPushButton:
        button = QPushButton("PUBLISH TDP")
        button.clicked.connect(self.__controller.set_publish_state)
        self.__layout.addWidget(button)
        return button
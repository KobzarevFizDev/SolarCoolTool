from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from Models.app_models import PreviewModeEnum

if TYPE_CHECKING:
    from Models.app_models import AppModel

class SelectedPreviewModeView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: AppModel = model
        self.model.add_observer(self)
        self.layout = QHBoxLayout()

        parentWindow.layout.addLayout(self.layout, 0, 2, 1, 2)

        self.__solar_preview_button = self.__create_solar_preview_button()
        self.__distance_plot_button = self.__create_distance_plot_preview()
        self.__distance_plot_debug_button = self.__create_test_mode_distance_plot_preview()

        self.model_is_changed()

    def model_is_changed(self):
        current_mode = self.model.selected_preview_mode.current_preview_mode
        self.__show_current_selected_mode(current_mode)

    def __show_current_selected_mode(self, current_mode: PreviewModeEnum):
        print(f"SelectedPreviewMode::current_mode = {current_mode}")
        buttons = {PreviewModeEnum.SOLAR_PREVIEW : self.__solar_preview_button,
                  PreviewModeEnum.DISTANCE_PLOT_PREVIEW : self.__distance_plot_button,
                  PreviewModeEnum.TEST_MODE_DISTANCE_PLOT_PREVIEW : self.__distance_plot_debug_button}
        for unselected_button in buttons.values():
            unselected_button.setStyleSheet("background-color: gray; color: white;")
        selected_button = buttons[current_mode]
        selected_button.setStyleSheet("background-color: green; color: white;")

    def __create_solar_preview_button(self) -> QPushButton:
        button = QPushButton("SOLAR PREVIEW")
        button.clicked.connect(self.__on_selected_solar_preview_mode)
        self.layout.addWidget(button)
        return button

    def __create_distance_plot_preview(self) -> QPushButton:
        button = QPushButton("DISTANCE PLOT")
        button.clicked.connect(self.__on_selected_distance_plot_mode)
        self.layout.addWidget(button)
        return button

    def __create_test_mode_distance_plot_preview(self) -> QPushButton:
        button = QPushButton("DISTANCE PLOT [DEBUG]")
        button.clicked.connect(self.__on_selected_distance_plot_debug_mode)
        self.layout.addWidget(button)
        return button

    def __on_selected_solar_preview_mode(self):
        self.model.selected_preview_mode.set_solar_preview_mode()
        self.model.notify_observers()

    def __on_selected_distance_plot_mode(self):
        self.model.selected_preview_mode.set_time_distance_mode()
        self.model.notify_observers()

    def __on_selected_distance_plot_debug_mode(self):
        self.model.selected_preview_mode.set_distance_plot_debug_mode()
        self.model.notify_observers()

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QFormLayout
from TimeDistancePlotBuilder.Models.app_models import AppStates
from PyQt5.QtCore import Qt

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Controllers.app_state_controller import AppStateController
    from TimeDistancePlotBuilder.Models.app_models import AppModel



class PusblishTdpView:
    def __init__(self, controller, model, parentWindow):
        self.__controller: AppStateController = controller
        self.__model: AppModel = model
        self.__model.add_observer(self)
        self.__layout = QHBoxLayout()
        self.__form = QFormLayout()

        self.__create_save_name_input()
        self.__create_email_input()
        self.__create_password_input()

        self.__layout.setAlignment(Qt.AlignCenter)
        self.__layout.addLayout(self.__form)


        parentWindow.layout.addLayout(self.__layout, 1, 2, 1, 1)

    def create_label(self, text):
        label = QLabel(text)
        label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)  # Запрещаем растяжение
        return label

    def model_is_changed(self):
        if self.__model.app_state.current_state == AppStates.PUBLISH_TDP_STATE:
            self.__show_all_widgets_in_layout(self.__form)
        else:
            self.__hide_all_widgets_in_layout(self.__form)

    def __create_save_name_input(self) -> None:
        save_label = QLabel("Save for publish: ")
        self.__save_input = QLineEdit()
        self.__form.addRow(save_label, self.__save_input)

    def __create_email_input(self) -> None:
        email_label = QLabel("Your email: ")
        self.__email_input = QLineEdit()
        # self.__email_input.setFixedWidth(200)
        self.__form.addRow(email_label, self.__email_input)
    
    
    def __create_password_input(self) -> None:
        password_label = QLabel("Your password: ")
        self.__password_input = QLineEdit()
        # self.__password_input.setFixedWidth(200)
        self.__form.addRow(password_label, self.__password_input)

    def __show_all_widgets_in_layout(self, layout) -> None:
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.show()
            elif item.layout():
                self.__show_all_widgets_in_layout(item.layout())

    def __hide_all_widgets_in_layout(self, layout) -> None:
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.hide()
            elif item.layout():
                self.__hide_all_widgets_in_layout(item.layout())
        
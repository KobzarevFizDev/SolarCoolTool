from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from TimeDistancePlotBuilder.Models.app_models import AppStates
from PyQt5.QtCore import Qt


if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Controllers.publish_tdp_controller import PublishTdpController
    from TimeDistancePlotBuilder.Models.app_models import AppModel



class PusblishTdpView:
    def __init__(self, controller, model, parentWindow):
        self.__controller: PublishTdpController = controller
        self.__model: AppModel = model
        self.__model.add_observer(self)
        self.__layout = QVBoxLayout()
        self.__form = QFormLayout()

        self.__create_title()
        self.__create_save_name_input()
        self.__create_email_input()
        self.__create_password_input()


        self.__layout.setAlignment(Qt.AlignCenter)
        self.__layout.addLayout(self.__form)

        self.__create_crud_buttons()

        parentWindow.layout.addLayout(self.__layout, 1, 2, 1, 1)


    def model_is_changed(self):
        if self.__model.app_state.current_state == AppStates.PUBLISH_TDP_STATE:
            self.__show_all_widgets_in_layout(self.__layout)
        else:
            self.__hide_all_widgets_in_layout(self.__layout)

    def __create_title(self) -> None:
        title = QLabel("TDPB.Magazine")
        title.setStyleSheet("font-size: 24px; color: blue; font-weight: bold;")
        self.__form.addWidget(title)

    def __create_save_name_input(self) -> None:
        save_label = QLabel("Save for publish: ")
        self.__save_input = QLineEdit()
        self.__form.addRow(save_label, self.__save_input)

    def __create_email_input(self) -> None:
        email_label = QLabel("Your email: ")
        self.__email_input = QLineEdit()
        self.__form.addRow(email_label, self.__email_input)
    
    def __create_password_input(self) -> None:
        password_label = QLabel("Your password: ")
        self.__password_input = QLineEdit()
        self.__form.addRow(password_label, self.__password_input)

    def __create_crud_buttons(self) -> None:
        self.__delete_button = QPushButton("DELETE")
        self.__publish_button = QPushButton("PUBLISH")
        self.__update_button = QPushButton("UPDATE")

        container = QHBoxLayout()

        self.__delete_button.clicked.connect(self.__controller.delete_tdp_from_cloud)
        self.__publish_button.clicked.connect(self.__controller.publish_tdp_to_cloud)
        self.__update_button.clicked.connect(self.__controller.update_tdp_in_cloud)

        container.addWidget(self.__delete_button)
        container.addWidget(self.__publish_button)
        container.addWidget(self.__update_button)

        self.__form.addRow(container)

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
        
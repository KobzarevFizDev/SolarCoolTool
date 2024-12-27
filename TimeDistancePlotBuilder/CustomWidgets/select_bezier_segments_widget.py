from typing import List

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class SelectBezierSegmentsWidget(QWidget):
    state_of_bezier_segment_was_changed = pyqtSignal(int)

    def __init__(self, parent):
        super(SelectBezierSegmentsWidget, self).__init__()
        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout)
        self.__buttons: List[QPushButton] = list()
        self.__create_buttons()

    def __create_buttons(self):
        for i in range(10):
            button = QPushButton()
            button.setProperty("id", i)
            button.setFixedSize(17,24)
            button.setText("")
            button.clicked.connect(self.__on_clicked)
            button.setStyleSheet("background-color: yellow; border: 2px solid black")
            self.__buttons.append(button)
            self.__layout.addWidget(button)

    def set_segment_as_selected(self, index: int) -> None:
        button: QPushButton = self.__buttons[index]
        button.setStyleSheet("background-color: yellow; border: 2px solid black")

    def set_segment_as_unselected(self, index: int) -> None:
        button: QPushButton = self.__buttons[index]
        button.setStyleSheet("background-color: blue; border: 2px solid black")

    def __on_clicked(self):
        clicked_button = self.sender()
        id: int = clicked_button.property('id')
        self.state_of_bezier_segment_was_changed.emit(id)
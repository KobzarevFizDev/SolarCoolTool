from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class ChannelSwitchWidget(QWidget):
    channelSwitchedSignal = pyqtSignal(int)
    def __init__(self, parent):
        super(ChannelSwitchWidget, self).__init__()
        self.setMinimumSize(200, 300)
        self.setMaximumSize(200, 300)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        hbox = QVBoxLayout()
        self.setLayout(hbox)

        self.A94_channel_button = QPushButton("A94")
        self.A131_channel_button = QPushButton("A131")
        self.A171_channel_button = QPushButton("A171")
        self.A193_channel_button = QPushButton("A193")
        self.A211_channel_button = QPushButton("A211")
        self.A355_channel_button = QPushButton("A355")

        hbox.addWidget(self.A94_channel_button)
        hbox.addWidget(self.A131_channel_button)
        hbox.addWidget(self.A171_channel_button)
        hbox.addWidget(self.A193_channel_button)
        hbox.addWidget(self.A211_channel_button)
        hbox.addWidget(self.A355_channel_button)

        self.A94_channel_button.clicked.connect(self.__switched_a94)
        self.A131_channel_button.clicked.connect(self.__switched_a131)
        self.A171_channel_button.clicked.connect(self.__switched_a171)
        self.A193_channel_button.clicked.connect(self.__switched_a193)
        self.A211_channel_button.clicked.connect(self.__switched_a211)
        self.A355_channel_button.clicked.connect(self.__switched_a355)

        self.buttons_map =  {94  : self.A94_channel_button,
                             131 : self.A131_channel_button,
                             171 : self.A171_channel_button,
                             193 : self.A193_channel_button,
                             211 : self.A211_channel_button,
                             355 : self.A355_channel_button}

    def mark_channel_as_selected(self, channel: int) -> None:
        button_of_selected_channel = self.__get_button_by_channel(channel)
        button_of_selected_channel.setStyleSheet("background-color: green; color: white;")
        button_of_selected_channel.setEnabled(True)

    def mark_channel_as_not_available(self, channel: int) -> None:
        button_of_not_available_channel = self.__get_button_by_channel(channel)
        button_of_not_available_channel.setStyleSheet("background-color: red; color: white;")
        button_of_not_available_channel.setEnabled(False)

    def mark_channel_as_available(self, channel: int) -> None:
        button_of_available_channel = self.__get_button_by_channel(channel)
        button_of_available_channel.setStyleSheet("background-color: blue; color: white;")
        button_of_available_channel.setEnabled(True)

    def __get_button_by_channel(self, channel: int) -> QPushButton:
        return self.buttons_map[channel]

    def __switched_a94(self):
        self.channelSwitchedSignal.emit(94)

    def __switched_a131(self):
        self.channelSwitchedSignal.emit(131)

    def __switched_a171(self):
        self.channelSwitchedSignal.emit(171)

    def __switched_a193(self):
        self.channelSwitchedSignal.emit(193)

    def __switched_a211(self):
        self.channelSwitchedSignal.emit(211)

    def __switched_a355(self):
        self.channelSwitchedSignal.emit(355)
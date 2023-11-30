from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

class ChannelSwitchWidget(QWidget):
    channelSwitchedSignal = pyqtSignal(int)
    def __init__(self, parent):
        super(ChannelSwitchWidget, self).__init__()
        self.setMinimumSize(200, 300)
        self.setMaximumSize(200, 300)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        #palette = self.palette()
        #palette.setColor(QPalette.Window, QColor(Qt.green))
        #self.setPalette(palette)
        hbox = QVBoxLayout()
        self.setLayout(hbox)

        self.A94ChannelButton = QPushButton("A94")
        self.A131ChannelButton = QPushButton("A131")
        self.A171ChannelButton = QPushButton("A171")
        self.A193ChannelButton = QPushButton("A193")
        self.A211ChannelButton = QPushButton("A211")
        self.A355ChannelButton = QPushButton("A355")

        hbox.addWidget(self.A94ChannelButton)
        hbox.addWidget(self.A131ChannelButton)
        hbox.addWidget(self.A171ChannelButton)
        hbox.addWidget(self.A193ChannelButton)
        hbox.addWidget(self.A211ChannelButton)
        hbox.addWidget(self.A355ChannelButton)

        self.A94ChannelButton.clicked.connect(self.__switchedA94)
        self.A131ChannelButton.clicked.connect(self.__switchedA131)
        self.A171ChannelButton.clicked.connect(self.__switchedA171)
        self.A193ChannelButton.clicked.connect(self.__switchedA193)
        self.A211ChannelButton.clicked.connect(self.__switchedA211)
        self.A355ChannelButton.clicked.connect(self.__switchedA355)

    def markChannelAsSelected(self, channel: int):
        buttons =  {94  : self.A94ChannelButton,
                    131 : self.A131ChannelButton,
                    171 : self.A171ChannelButton,
                    193 : self.A193ChannelButton,
                    211 : self.A211ChannelButton,
                    355 : self.A355ChannelButton}
        for b in buttons.values():
            b.setStyleSheet("background-color: green; color: white;")
        buttons[channel].setStyleSheet("background-color: blue; color: white;")


    def __switchedA94(self):
        self.channelSwitchedSignal.emit(94)

    def __switchedA131(self):
        self.channelSwitchedSignal.emit(131)

    def __switchedA171(self):
        self.channelSwitchedSignal.emit(171)

    def __switchedA193(self):
        self.channelSwitchedSignal.emit(193)

    def __switchedA211(self):
        self.channelSwitchedSignal.emit(211)

    def __switchedA355(self):
        self.channelSwitchedSignal.emit(355)
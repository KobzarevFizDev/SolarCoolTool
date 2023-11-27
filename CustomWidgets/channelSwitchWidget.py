from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget


class ChannelSwitchWidget(QWidget):
    def __init__(self, parent):
        super(ChannelSwitchWidget, self).__init__()
        self.setMinimumSize(200, 300)
        self.setMaximumSize(200, 300)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.green))
        self.setPalette(palette)
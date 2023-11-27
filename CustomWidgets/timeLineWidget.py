from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget

class TimeLineWidget(QWidget):
    def __init__(self, parent):
        super(TimeLineWidget, self).__init__()
        self.setMinimumSize(900, 300)
        self.setMaximumSize(900, 300)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.red))
        self.setPalette(palette)


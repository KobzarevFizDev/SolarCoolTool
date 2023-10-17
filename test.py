import sys
from PyQt5 import QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Widget")
        self.setGeometry(100, 100, 400, 300)

        # Create a label
        self.label = QtWidgets.QLabel("Hello World", self)
        self.label.move(150, 150)

    def some_feature(self):
        # Example of a feature that could be tested
        return 42
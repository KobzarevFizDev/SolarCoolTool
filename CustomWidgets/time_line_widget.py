from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout

minValueOfTimeLineSlider = 0
maxValueOfTimeLineSlider = 200

class TimeLineWidget(QWidget):
    selected_image_in_channel = pyqtSignal(int)
    def __init__(self, parent):
        super(TimeLineWidget, self).__init__()
        self.setMinimumSize(1000, 300)
        self.setMaximumSize(1000, 300)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.red))
        self.setPalette(palette)

        layout = QHBoxLayout()
        self.setLayout(layout)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(minValueOfTimeLineSlider,maxValueOfTimeLineSlider)
        self.slider.valueChanged.connect(self.change_value_of_slider)
        layout.addWidget(self.slider)
        #self.set_number_images_in_channel(181)

    def set_number_images_in_channel(self, number_of_images_in_channel: int):
        self.number_of_images_in_channel = number_of_images_in_channel

    def change_value_of_slider(self, value):
        step = (self.number_of_images_in_channel - 1) / maxValueOfTimeLineSlider
        index_of_image = int(value*step)
        self.selected_image_in_channel.emit(index_of_image)



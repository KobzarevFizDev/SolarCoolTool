from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout

minValueOfTimeLineSlider = 0
maxValueOfTimeLineSlider = 200

class TimeLineWidget(QWidget):
    selectedImageInChannel = pyqtSignal(int)
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
        self.slider.valueChanged.connect(self.changeValueOfSlider)
        layout.addWidget(self.slider)
        #self.setNumberImagesInChannel(181)

    def setNumberImagesInChannel(self, numberOfImagesInChannel: int):
        self.numberOfImagesInChannel = numberOfImagesInChannel

    def changeValueOfSlider(self, value):
        step = (self.numberOfImagesInChannel-1)/maxValueOfTimeLineSlider
        indexOfImage = int(value*step)
        self.selectedImageInChannel.emit(indexOfImage)





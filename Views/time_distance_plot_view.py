from typing import TYPE_CHECKING
import numpy.typing as npt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QPushButton, QHBoxLayout

from CustomWidgets.time_distance_plot_widget import TimeDistancePlotWidget
from Models.app_models import PreviewModeEnum

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.time_distance_plot_controller import TimeDistancePlotController



class TimeDistancePlotView:
    def __init__(self, controller, model, parentWindow):
        self.controller: TimeDistancePlotController = controller
        self.model: AppModel = model

        self.layout = QVBoxLayout()


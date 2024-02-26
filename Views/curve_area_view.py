import math
from typing import TYPE_CHECKING

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage, QPixmap

from CustomWidgets.curve_area_widget import CurveAreaWidget

if TYPE_CHECKING:
    from Models.solar_editor_model import SolarEditorModel
    from Controllers.mask_spline_controller import MaskSplineConroller

class CurveAreaView:
    def __init__(self, controller, model, parentWindow):
        self.controller: MaskSplineConroller = controller
        self.model: SolarEditorModel = model
        self.widget = CurveAreaWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 0, 0, 1, 2)
        self.model.addObserver(self)
        self.widget.mouseDoubleClickSignal.connect(self.createNewPointWidget)
        self.widget.drawMask(self.model.maskSpline, self.model)

    def createNewPointWidget(self, x, y):
        self.controller.createNewPoint(x, y)

    def modelIsChanged(self):
        currentSolarImage: QImage = self.model.currentSolarImageAsQTImage
        topLeft, bottomRight = self.model.solarViewModel.selectedPlotInImage
        mask = QRect(topLeft, bottomRight)
        pixmapOfSolarPlot = QPixmap.fromImage(currentSolarImage.copy(mask))
        pixmapOfSolarPlot = pixmapOfSolarPlot.scaled(600, 600)

        self.widget.updateSolarPlot(pixmapOfSolarPlot)
        if self.model.maskSpline.isAvailableToDraw:
            self.widget.updateSpline(self.model.maskSpline)

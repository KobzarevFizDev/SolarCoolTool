from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint

from CustomWidgets.solar_viewer_widget import SolarViewerWidget

if TYPE_CHECKING:
    from Models.solar_editor_model import SolarEditorModel
    from Controllers.solar_viewer_controller import SolarViewerController

class SolarViewerView:
    def __init__(self, controller, model, parentWindow):
        self.controller: SolarViewerController = controller
        self.model: SolarEditorModel = model
        self.widget: SolarViewerWidget = SolarViewerWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget,0,2,1,1)
        self.model.addObserver(self)
        self.widget.wheelScrollSignal.connect(self.zoom)
        self.widget.mouseMoveSignal.connect(self.move)
        self.widget.plotWasAllocatedSignal.connect(self.selectedPlot)

    def zoom(self, x, y):
        if y > 0:
            self.controller.increaseZoom(0.05)
        else:
            self.controller.decreaseZoom(0.05)

    def move(self, x, y):
        self.controller.moveSolarImage(QPoint(x,y))

    def selectedPlot(self, topLeftPoint: QPoint, bottomRightPoint: QPoint):
        self.controller.selectPlotOfImage(topLeftPoint, bottomRightPoint)
        #print("SELECTED = {0} <-> {1}".format((topLeftPoint.x(), topLeftPoint.y()), (bottomRightPoint.x(), bottomRightPoint.y())))


    def modelIsChanged(self):
        solarImage = self.model.currentSolarImage
        scale = self.model.solarViewModel.zoom * self.model.solarViewModel.originImageScale
        offset = self.model.solarViewModel.offset
        zoom = self.model.solarViewModel.zoom
        self.widget.displayImage(solarImage, scale, zoom, offset)

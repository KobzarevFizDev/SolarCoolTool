from CustomWidgets.solarViewerWidget import SolarViewerWidget
from Models.solarViewerModel import SolarViewModel

class SolarViewerView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: SolarViewModel = model
        self.widget: SolarViewerWidget = SolarViewerWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget,0,1)
        self.model.addObserver(self)
        self.widget.wheelScrollSignal.connect(self.zoom)

    def zoom(self, x, y):
        if y > 0:
            self.controller.increaseZoom(0.05)
        else:
            self.controller.decreaseZoom(0.05)

    def modelIsChanged(self):
        self.widget.setScaleOfSolarView(self.model.zoom * self.model.originScaleImage)

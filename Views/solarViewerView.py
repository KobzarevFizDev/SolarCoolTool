from CustomWidgets.solarViewerWidget import SolarViewerWidget

class SolarViewerView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget: SolarViewerWidget = SolarViewerWidget(parentWindow)
        #row column
        parentWindow.layout.addWidget(self.widget,0,2,1,1)
        self.model.addObserver(self)
        self.widget.wheelScrollSignal.connect(self.zoom)

    def zoom(self, x, y):
        if y > 0:
            self.controller.increaseZoom(0.05)
        else:
            self.controller.decreaseZoom(0.05)

    def modelIsChanged(self):
        self.widget.setScaleOfSolarView(self.model.zoom * self.model.originImageScale)

from Views.solarViewerView import SolarViewerView

class SolarViewerController:
    def __init__(self, model, mainAppWindow):
        self.model = model
        self.view = SolarViewerView(self, model, mainAppWindow)

    def increaseZoom(self, delta):
        self.model.changeZoom(delta)


    def decreaseZoom(self, delta):
        self.model.changeZoom(-delta)
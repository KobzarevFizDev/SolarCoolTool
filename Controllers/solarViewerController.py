from Views.solarViewerView import SolarViewerView

class SolarViewerController:
    def __init__(self, model, mainAppWindow):
        self.model = model
        self.view = SolarViewerView(self, model, mainAppWindow)
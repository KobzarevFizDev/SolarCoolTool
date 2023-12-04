from Views.solar_viewer_view import SolarViewerView
from Models.solar_editor_model import SolarEditorModel

class SolarViewerController:
    def __init__(self, model, mainAppWindow):
        self.model: SolarEditorModel = model
        self.view = SolarViewerView(self, model, mainAppWindow)

    def moveImage(self, deltaPosition):
        self.model.solarViewModel.moveImage(deltaPosition)
        self.model.notifyObservers()

    def increaseZoom(self, delta):
        self.model.solarViewModel.changeZoom(delta)
        self.model.notifyObservers()


    def decreaseZoom(self, delta):
        self.model.solarViewModel.changeZoom(-delta)
        self.model.notifyObservers()
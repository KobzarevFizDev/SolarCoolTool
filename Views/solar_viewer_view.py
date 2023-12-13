from typing import TYPE_CHECKING
from CustomWidgets.solar_viewer_widget import SolarViewerWidget

if TYPE_CHECKING:
    from Models.solar_editor_model import SolarEditorModel

class SolarViewerView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: SolarEditorModel = model
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
        self.widget.setScaleOfSolarView(self.model.solarViewModel.zoom * self.model.solarViewModel.originImageScale)
        self.widget.displayImage(self.model.currentSolarImage)

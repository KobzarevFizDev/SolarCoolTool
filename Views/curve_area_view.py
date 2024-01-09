from typing import TYPE_CHECKING
from CustomWidgets.curve_area_widget import CurveAreaWidget

if TYPE_CHECKING:
    from Models.solar_editor_model import SolarEditorModel
    from Controllers.mask_spline_controller import MaskSplineConroller

class CurveAreaView:
    def __init__(self, controller, model, parentWindow):
        self.controller: MaskSplineConroller = controller
        self.model: SolarEditorModel = model
        self.widget = CurveAreaWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget,0,0,1,2)
        self.model.addObserver(self)
        self.widget.mouseDoubleClickSignal.connect(self.createNewPointWidget)
        self.widget.drawSplineCurve(self.model.maskSpline, 10, self.model)

    def createNewPointWidget(self, x, y):
        self.controller.createNewPoint(x, y)

    def modelIsChanged(self):
        if self.model.maskSpline.isAvailableToDraw:
            self.widget.updateSplineCurve(self.model.maskSpline, 10)

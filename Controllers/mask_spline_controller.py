from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint

from Views.curve_area_view import CurveAreaView

if TYPE_CHECKING:
    from Models.solar_editor_model import SolarEditorModel


class MaskSplineConroller:
    def __init__(self, model, mainAppWindow):
        self.model: SolarEditorModel = model
        self.view = CurveAreaView(self, model, mainAppWindow)

    def createNewPoint(self, x, y):
        newPoint = QPoint(x, y)
        self.model.maskSpline.addAnchor(newPoint)
        self.model.notifyObservers()
        return newPoint

    def deletePoint(self, point):
        self.model.maskSpline.removeLastAnchor()
        self.model.notifyObservers()

    def increaseNumberOfSegments(self):
        self.model.maskSpline.increaseNumberOfSegments()
        self.model.notifyObservers()

    def decreaseNumberOfSegments(self):
        self.model.maskSpline.decreaseNumberOfSegments()
        self.model.notifyObservers()
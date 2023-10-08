from Views.curveAreaView import CurveAreaView
class CurveEditorController:
    def __init__(self, model, MainAppWindow):
        self.model = model
        self.view = CurveAreaView(self, model, MainAppWindow)

    def addPoint(self, point):
        self.model.addPoint(point)
        self.view.drawArea(self.model.getPoints())

    def removePoint(self, point):
        self.model.removePoint(point)
        self.view.drawArea(self.model.getPoints())
from Views.curveAreaView import CurveAreaView
class CurveEditorController:
    def __init__(self, model, MainAppWindow):
        self.model = model
        self.view = CurveAreaView(self, model, MainAppWindow)

    def createPoint(self, x, y):
        print("create point: {0}, {1}".format(x,y))
        #self.model.addPoint(point)
        #self.view.drawArea(self.model.getPoints())

    def deletePoint(self, x,y):
        print("delete point: {0}, {1}".format(x, y))
        #self.model.removePoint(point)
        #self.view.drawArea(self.model.getPoints())
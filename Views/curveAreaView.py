from CustomWidgets.curveAreaWidget import CurveAreaWidget
from Models.curveAreaModel import Point


class CurveAreaView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = CurveAreaWidget(parentWindow)
        parentWindow.setCentralWidget(self.widget)
        self.model.addObserver(self)
        self.widget.mouseDoubleClickSignal.connect(self.createNewPointWidget)
        #self.widget.mouseDoubleClickSignal.connect(self.controller.createNewPoint)

    def createNewPointWidget(self, x, y):
        pointModel = Point(x, y)
        self.widget.drawNewPoint(pointModel, self.model)

    def modelIsChanged(self):
        print("Model is changed {0}".format([p.x for p in self.model.getPoints()]))


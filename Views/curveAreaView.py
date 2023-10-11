from CustomWidgets.curveAreaWidget import CurveAreaWidget

class CurveAreaView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = CurveAreaWidget(parentWindow)
        parentWindow.setCentralWidget(self.widget)
        self.model.addObserver(self)
        self.widget.mouseDoubleClickSignal.connect(self.controller.createNewPoint)
        self.widget.mouseMoveSignal.connect(self.controller.mouseMove)

    def modelIsChanged(self):
        print("Model is changed {0}".format([p.x for p in self.model.getPoints()]))
        self.widget.drawPoints(self.model.getPoints())
        #self.widget.drawArea(self.model.getPoints())

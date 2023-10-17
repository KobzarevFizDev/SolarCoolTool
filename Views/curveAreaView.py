from CustomWidgets.curveAreaWidget import CurveAreaWidget


class CurveAreaView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = CurveAreaWidget(parentWindow)
        parentWindow.setCentralWidget(self.widget)
        self.model.addObserver(self)
        self.widget.mouseDoubleClickSignal.connect(self.createNewPointWidget)

    def createNewPointWidget(self, x, y):
        self.controller.createNewPoint(x, y)

    def modelIsChanged(self):
        self.widget.clearAll()
        for p in self.model.getPoints():
            self.widget.drawPoint(p, self.model, self.controller)

        if self.model.numberOfPoints > 3:
            points = self.controller.calculatePointsFormingBrokenLine()
            self.controller.calculateAreaSegments(points, 20)
            self.widget.drawLine(points)

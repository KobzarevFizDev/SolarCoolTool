from CustomWidgets.curveAreaWidget import CurveAreaWidget

class CurveAreaView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = CurveAreaWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget,0,0,1,2)
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
            topPoints = self.controller.calculateTopPointsFormingArea(points, 20)
            bottomPoints = self.controller.calculateBottomPointsFormingArea(points, 20)
            segments = self.controller.calculateAreaSegments(topPoints, bottomPoints)
            self.controller.calculateAreaSegments(points, bottomPoints)
            self.widget.drawCurve(points)
            self.widget.drawAreaSegments(segments)

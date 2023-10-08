from CustomWidgets.curveAreaWidget import CurveAreaWidget

class CurveAreaView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = CurveAreaWidget(parentWindow)
        parentWindow.setCentralWidget(self.widget)


    def modelIsChanged(self):
        self.widget.drawPoints(self.model.getPoints())

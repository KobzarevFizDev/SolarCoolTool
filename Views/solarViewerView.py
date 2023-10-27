from  CustomWidgets.solarViewerWidget import SolarViewerWidget

class SolarViewerView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = SolarViewerWidget(parentWindow)
        #parentWindow.setCentralWidget(self.widget)
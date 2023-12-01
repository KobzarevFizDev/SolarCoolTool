from CustomWidgets.time_line_widget import TimeLineWidget


class TimeLineView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = TimeLineWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 1, 1, 3)
        self.model.addObserver(self)
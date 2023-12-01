from Views.timeLineView import TimeLineView


class TimeLineController:
    def __init__(self, model, mainAppWindow):
        self.model = model
        self.view = TimeLineView(self, model, mainAppWindow)
from CustomWidgets.time_line_widget import TimeLineWidget
from Models.solar_editor_model import SolarEditorModel
import images_indexer

class TimeLineView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: SolarEditorModel = model
        self.widget = TimeLineWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 1, 1, 3)
        self.model.addObserver(self)

    def modelIsChanged(self):
        print("TimeLineView. modelIsChanged")
        print("Current channel = {0}".format(self.model.currentChannelModel.currentChannel))
        #print("Number of images = {0}".format(images_indexer.))

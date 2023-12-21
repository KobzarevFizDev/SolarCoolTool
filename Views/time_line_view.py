from CustomWidgets.time_line_widget import TimeLineWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.solar_editor_model import SolarEditorModel
    from Controllers.time_line_controller import TimeLineController

class TimeLineView:
    def __init__(self, controller, model, parentWindow):
        self.controller: TimeLineController = controller
        self.model: SolarEditorModel = model
        self.widget = TimeLineWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 1, 1, 3)
        self.model.addObserver(self)
        self.widget.selectedImageInChannel.connect(self.selectedImage)

    def selectedImage(self, indexOfImage: int) -> None:
        self.controller.selectImage(indexOfImage)

    def modelIsChanged(self):
        numberImagesInChannel = self.model.currentChannelModel.numberOfImagesInChannel
        self.widget.setNumberImagesInChannel(numberImagesInChannel)
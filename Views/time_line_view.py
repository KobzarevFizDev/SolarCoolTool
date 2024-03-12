from CustomWidgets.time_line_widget import TimeLineWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Models.app_models import AppModel
    from Controllers.time_line_controller import TimeLineController

class TimeLineView:
    def __init__(self, controller, model, parentWindow):
        self.controller: TimeLineController = controller
        self.model: AppModel = model
        self.widget = TimeLineWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 1, 1, 3)
        self.model.add_observer(self)
        self.widget.selected_image_in_channel.connect(self.selected_image)

        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.widget.set_number_images_in_channel(number_images_in_channel)


    def selected_image(self, indexOfImage: int) -> None:
        self.controller.select_image(indexOfImage)

    def model_is_changed(self):
        number_images_in_channel = self.model.current_channel.number_of_images_in_current_channel
        self.widget.set_number_images_in_channel(number_images_in_channel)
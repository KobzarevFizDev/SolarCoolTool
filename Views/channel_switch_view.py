from typing import TYPE_CHECKING
from CustomWidgets.channel_switch_widget import ChannelSwitchWidget

if TYPE_CHECKING:
    from Models.app_models import AppModel

class ChannelSwitchView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: AppModel = model
        self.widget = ChannelSwitchWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 2, 0)
        self.model.add_observer(self)
        self.widget.channelSwitchedSignal.connect(self.switch_channel)
        self.paint_buttons_according_model()

    def switch_channel(self, channel: int):
        self.controller.switch_channel(channel)

    def model_is_changed(self):
        self.paint_buttons_according_model()

    def paint_buttons_according_model(self):
        not_available_channels = self.model.current_channel.not_available_channels
        for not_available_channel in not_available_channels:
            self.widget.mark_channel_as_not_available(not_available_channel)

        available_channels = self.model.current_channel.available_channels
        for available_channel in available_channels:
            self.widget.mark_channel_as_available(available_channel)

        current_channel = self.model.current_channel.channel
        self.widget.mark_channel_as_selected(current_channel)

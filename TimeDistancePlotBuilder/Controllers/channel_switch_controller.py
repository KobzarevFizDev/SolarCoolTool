from Views.channel_switch_view import ChannelSwitchView
from Models.app_models import AppModel

class ChannelSwitchController:
    def __init__(self, model, mainAppWindow):
        self.model: AppModel = model
        self.view = ChannelSwitchView(self, model, mainAppWindow)

    def switch_channel(self, channel: int):
        self.model.current_channel.channel = channel
        self.model.solar_frames_storage.cache_channel(channel)
        self.model.notify_observers()

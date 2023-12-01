from Views.channel_switch_view import ChannelSwitchView
from Models.solar_editor_model import CurrentChannelModel

class ChannelSwitchController:
    def __init__(self, model, mainAppWindow):
        self.model: CurrentChannelModel = model
        self.view = ChannelSwitchView(self, model, mainAppWindow)

    def switchChannel(self, channel:int):
        self.model.setCurrentChannel(channel)
        self.model.notifyObservers()
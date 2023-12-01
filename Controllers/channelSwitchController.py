from Views.channelSwitchView import ChannelSwitchView


class ChannelSwitchController:
    def __init__(self, model, mainAppWindow):
        self.model = model
        self.view = ChannelSwitchView(self, model, mainAppWindow)

    def switchChannel(self, channel:int):
        self.model.channel = channel
        self.model.notifyObservers()
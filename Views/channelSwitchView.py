from CustomWidgets.channelSwitchWidget import ChannelSwitchWidget


class ChannelSwitchView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = ChannelSwitchWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 0)
        self.model.addObserver(self)
        self.widget.channelSwitchedSignal.connect(self.switchChannel)

    def switchChannel(self, channel:int):
        self.controller.switchChannel(channel)

    def modelIsChanged(self):
        print("channel switch view model was changed")
        self.widget.markChannelAsSelected(self.model.channel)
        # TODO: Закрасить выбранную кнопку
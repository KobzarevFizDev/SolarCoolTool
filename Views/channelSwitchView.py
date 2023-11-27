from CustomWidgets.channelSwitchWidget import ChannelSwitchWidget


class ChannelSwitchView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model = model
        self.widget = ChannelSwitchWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 0)

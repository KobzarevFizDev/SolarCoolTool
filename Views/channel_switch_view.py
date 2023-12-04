from CustomWidgets.channel_switch_widget import ChannelSwitchWidget
from Models.solar_editor_model import SolarEditorModel

class ChannelSwitchView:
    def __init__(self, controller, model, parentWindow):
        self.controller = controller
        self.model: SolarEditorModel = model
        self.widget = ChannelSwitchWidget(parentWindow)
        parentWindow.layout.addWidget(self.widget, 1, 0)
        self.model.addObserver(self)
        self.widget.channelSwitchedSignal.connect(self.switchChannel)
        self.paintButtonsAccordingModel()

    def switchChannel(self, channel: int):
        self.controller.switchChannel(channel)

    def modelIsChanged(self):
        self.paintButtonsAccordingModel()

    def paintButtonsAccordingModel(self):
        for notAvailableChannel in self.model.currentChannelModel.notAvailableChannels:
            self.widget.markChannelAsNotAvailable(notAvailableChannel)

        for availableChannel in self.model.currentChannelModel.availableChannels:
            self.widget.markChannelAsAvailable(availableChannel)

        self.widget.markChannelAsSelected(self.model.currentChannelModel.currentChannel)
from TimeDistancePlotBuilder.Popups.popups import PopupManager
from TimeDistancePlotBuilder.Views.channel_switch_view import ChannelSwitchView
from TimeDistancePlotBuilder.Models.app_models import AppModel
from PyQt5.QtCore import QThread

class ChannelSwitchController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view = ChannelSwitchView(self, model, mainAppWindow)
        self.__popups_manager: PopupManager = mainAppWindow.popup_manager

    def switch_channel(self, channel: int) -> None:
        self.__popups_manager.loading_program_popup.show()

        self.__thread_load_frames = QThread()
        self.__worker = self.__model.solar_frames_storage
        self.__worker.moveToThread(self.__thread_load_frames)

        self.__worker.progress.connect(self.__popups_manager.loading_program_popup.update_progress)
        self.__thread_load_frames.started.connect(lambda: self.__worker.load_channel(channel))
        self.__worker.finished.connect(self.__thread_load_frames.quit)
        self.__worker.finished.connect(self.__worker.deleteLater)
        self.__thread_load_frames.finished.connect(self.__thread_load_frames.deleteLater)
        self.__thread_load_frames.finished.connect(lambda: self.__on_loaded_solar_frames(channel))

        self.__thread_load_frames.start()

    def __on_loaded_solar_frames(self, channel: int) -> None:
        self.__model.current_channel.channel = channel
        self.__model.notify_observers()
        self.__popups_manager.loading_program_popup.hide()

from TimeDistancePlotBuilder.Models.app_models import AppModel
from TimeDistancePlotBuilder.Views.publish_tdp_view import PusblishTdpView


class PublishTdpController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view: PusblishTdpView = PusblishTdpView(self, model, mainAppWindow)

    def publish_tdp_to_cloud(self) -> None:
        pass

    def delete_tdp_from_cloud(self) -> None:
        pass

    def update_tdp_in_cloud(self) -> None:
        pass
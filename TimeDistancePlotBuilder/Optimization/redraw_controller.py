from typing import TYPE_CHECKING
from TimeDistancePlotBuilder.Controllers.time_distance_plot_controller import TimeDistancePlotController

# if TYPE_CHECKING:
#     from TimeDistancePlotBuilder.app import AppModel


# class RedrawTdpController:
#     def __init__(self, controller: TimeDistancePlotController, app_model: AppModel):
#         self.__controller = controller
#         self.__model = app_model

        
#         self.__previous_tdp_step: int = 0
#         self.__is_new_tdp_build: bool = False

#     @property
#     def need_to_update_tdp_pixmap(self) -> bool:
#         is_new_tdp_build = self.__is_new_tdp_build
#         if is_new_tdp_build:
#             current_tdp_step: int = self.__model.time_line.tdp_step
#             is_tdp_step_changed = not self.__previous_tdp_step == current_tdp_step
#             return is_tdp_step_changed and self.__controller.is_middle_tdp_segment()
#         else:
#             return True
        

from typing import TYPE_CHECKING
from typing import Tuple, List
import numpy.typing as npt
from datetime import datetime

import os


from TimeDistancePlotBuilder.Models.app_models import AppModel
from TimeDistancePlotBuilder.Views.time_distance_plot_view import TimeDistancePlotView

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import Cubedata
    from TimeDistancePlotBuilder.Popups.popups import PopupManager

class TimeDistancePlotController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view: TimeDistancePlotView = TimeDistancePlotView(self, model, mainAppWindow)
        self.__popup_manager: PopupManager = mainAppWindow.popup_manager 

    def set_current_tdp_step(self, step: int) -> None:
        self.__model.time_line.tdp_step = step
        self.__model.notify_observers()

    def set_smooth_parametr(self, smooth_parametr_slider_value: int) -> None:
        smooth_parametr_value = float(smooth_parametr_slider_value) / 100
        self.__model.time_distance_plot.set_smooth_parametr(smooth_parametr_value)

    def set_range_of_tdp_build(self, range) -> None:
        start_frame_index: int = range[0]
        finish_frame_index: int = range[1]
        self.__model.time_line.start_frame_to_build_tdp = start_frame_index
        self.__model.time_line.finish_frame_to_build_tdp = finish_frame_index
        self.__model.notify_observers()

    def build_time_distance_plot(self, is_uniformly: bool) -> None:
        start_index: int = self.__model.time_line.start_frame_to_build_tdp
        finish_index: int = self.__model.time_line.finish_frame_to_build_tdp
        cubedata: Cubedata = self.__model.solar_frames_storage.get_cubedata_by_interval(start_index, finish_index)
        channel: int = self.__model.current_channel.channel
        number_of_skip_frames: int = self.__model.configuration.get_step_for_channel(channel)

        self.__popup_manager.process_popup.activate(process_description="Time distance plot is building")

        self.build_thread = QThread()
        self.worker = self.__model.time_distance_plot
        self.worker.moveToThread(self.build_thread)

        self.build_thread.started.connect(lambda: self.worker.build(number_of_skip_frames, cubedata, channel, is_uniformly))
        self.worker.finished.connect(self.build_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.build_thread.finished.connect(self.build_thread.deleteLater)
        self.build_thread.finished.connect(self.__model.notify_observers)
        self.build_thread.finished.connect(self.__popup_manager.process_popup.close)
        self.worker.progress.connect(lambda step, max_step: self.__popup_manager.process_popup.update_progress(int(step/max_step * 100)))

        self.build_thread.start()

    def debug_build_time_distance_plot(self) -> None:
        number_of_frames = self.__model.time_line.max_index_of_solar_frame_for_debug_tdp
        self.__model.time_distance_plot.build_test_tdp(number_of_frames)
        self.__model.notify_observers()

    def get_borders_of_tdp_step(self) -> Tuple[int, int]:
        current_tdp_step: int = self.__model.time_line.tdp_step
        visible_tdp_segment_in_steps: int = self.__view.tdp_widget_horizontal_size_in_steps
        half_visible_tdp_segment_in_steps: int = visible_tdp_segment_in_steps // 2
        width_of_tdp_steps: int = self.__model.time_distance_plot.width_of_tdp_step
        total_tdp_steps: int = self.__model.time_distance_plot.total_tdp_steps

        if (0 <= current_tdp_step) and (current_tdp_step < half_visible_tdp_segment_in_steps):
            start = current_tdp_step * width_of_tdp_steps
            finish = (current_tdp_step + 1) * width_of_tdp_steps
            return [start, finish]

        elif (half_visible_tdp_segment_in_steps <= current_tdp_step) and (current_tdp_step < total_tdp_steps - half_visible_tdp_segment_in_steps):
            start = self.__view.tdp_widget_horizontal_size_in_px // 2
            finish = start + width_of_tdp_steps
            return [start, finish]

        else:
            steps_left_to_tdp_end = total_tdp_steps - current_tdp_step
            start = self.__view.tdp_widget_horizontal_size_in_px - (steps_left_to_tdp_end - 1) * width_of_tdp_steps
            finish = start + width_of_tdp_steps
            return [start, finish]

    def get_borders_of_visible_tdp_segment_in_tdp_steps(self) -> Tuple[int, int]:
        current_tdp_step: int = self.__model.time_line.tdp_step
        visible_tdp_segment_in_steps: int = self.__view.tdp_widget_horizontal_size_in_steps
        half_visible_tdp_segment_in_steps: int = visible_tdp_segment_in_steps // 2
        total_tdp_steps = self.__model.time_distance_plot.total_tdp_steps 

        if (0 <= current_tdp_step) and (current_tdp_step < half_visible_tdp_segment_in_steps):
            return (0, visible_tdp_segment_in_steps - 1)
        elif (half_visible_tdp_segment_in_steps <= current_tdp_step) and (current_tdp_step < self.__model.time_distance_plot.total_tdp_steps - half_visible_tdp_segment_in_steps):
            offset_from_start_in_steps = (current_tdp_step - half_visible_tdp_segment_in_steps)
            return (offset_from_start_in_steps, offset_from_start_in_steps + visible_tdp_segment_in_steps - 1)
        else:
            return (total_tdp_steps - visible_tdp_segment_in_steps, total_tdp_steps - 1)
    
    def is_middle_tdp_segment(self) -> bool:
        current_tdp_step: int = self.__model.time_line.tdp_step
        visible_tdp_segment_in_steps: int = self.__view.tdp_widget_horizontal_size_in_steps
        half_visible_tdp_segment_in_steps: int = visible_tdp_segment_in_steps // 2
        return (half_visible_tdp_segment_in_steps <= current_tdp_step) and (current_tdp_step < self.__model.time_distance_plot.total_tdp_steps - half_visible_tdp_segment_in_steps) 


    def export_tdp(self) -> None:
        tdp_as_pixmap: QPixmap = self.__model.time_distance_plot.get_full_pixmap()
        tdp_as_numpy: npt.NDArray = self.__model.time_distance_plot.tdp_array

        frames_for_create_mp4: List[npt.NDArray] = self.__model.loop_animation.get_frames_for_animation()
        path_to_export: str = self.__create_directory_for_export()

        self.__popup_manager.export_tdp_popup.activate(tdp_as_numpy, tdp_as_pixmap, frames_for_create_mp4, path_to_export)

    def __create_directory_for_export(self) -> str:
        now = datetime.now()
        year:int = now.year
        month: int = now.month
        day: int = now.day
        hour: int = now.hour
        minutes: int = now.minute
        second: int = now.second
        new_directory_name = f"Export_Data_{year}_{month}_{day}_{hour}_{minutes}_{second}"
        path_to_export = os.path.join(self.__model.configuration.path_to_export_results, new_directory_name)
        os.mkdir(path_to_export)
        return path_to_export


    # todo: Легаси
    # def export_time_distance_plot(self) -> None:
    #     path_to_dir_to_export_result = self.__create_dir_to_save_export_data()
    #     self.__export_time_distance_plot_as_png(path_to_dir_to_export_result)
    #     self.__export_time_distance_plot_as_numpy_array(path_to_dir_to_export_result)
    #     self.__export_metadata_of_time_distance_plot_as_txt_file(path_to_dir_to_export_result)

    # def __create_dir_to_save_export_data(self) -> str:
    #     all_result_dirs = [d for d in os.listdir(self.__model.path_to_export_result) if os.path.isdir(os.path.join(self.__model.path_to_export_result, d))]
    #     result_dirs = [d for d in all_result_dirs if "result" in d]
    #     new_result_index = len(result_dirs) + 1
    #     name_of_dir_for_save_export_data = f"result {new_result_index}"
    #     path_to_dir_to_export_result = os.path.join(self.__model.path_to_export_result, name_of_dir_for_save_export_data)
    #     os.mkdir(path_to_dir_to_export_result)
    #     return path_to_dir_to_export_result

    # def __export_time_distance_plot_as_png(self, path_of_dir_to_export_result: str) -> None:
    #     current_channel: int = self.__model.current_channel.channel
    #     path_to_save_time_distance_plot_as_png = os.path.join(path_of_dir_to_export_result, f"time_distance_plot_A{current_channel}.png")
    #     self.__time_distance_plot.save_as_png(path_to_save_time_distance_plot_as_png, current_channel)

    # def __export_time_distance_plot_as_numpy_array(self, path_of_dir_to_export_result: str) -> None:
    #     current_channel: int = self.__model.current_channel.channel
    #     numpy_array_file_name = f"tdp_A{current_channel}.npy"
    #     path_to_save_time_distance_plot_as_numpy_array = os.path.join(path_of_dir_to_export_result, numpy_array_file_name)
    #     self.__time_distance_plot.save_numpy_array(path_to_save_time_distance_plot_as_numpy_array)

    # def __export_metadata_of_time_distance_plot_as_txt_file(self, path_of_dir_to_export_result: str) -> None:
        # current_channel: int = self.__model.current_channel.channel
        # metadata_file_name = f"tdp_A{current_channel}_metadata.txt"
        # path_to_metadata_file = os.path.join(path_of_dir_to_export_result, metadata_file_name)

        # content_of_metadata_file = []
        # number_of_slice_along_loop_head = "NUMBER_OF_SLICE_ALONG_LOOP=200 \n"
        # number_of_segments_bezier_curve_head = "NUMBER_OF_SEGMENTS_BEZIER_CURVE=10 \n"
        # channel_head = f"CHANNEL={current_channel} \n"
        # number_of_pixels_per_time_step_head = "NUMBER_OF_PIXELS_PER_TIME_STEP=3 \n"

        # content_of_metadata_file.append(number_of_slice_along_loop_head)
        # content_of_metadata_file.append(number_of_segments_bezier_curve_head)
        # content_of_metadata_file.append(channel_head)
        # content_of_metadata_file.append(number_of_pixels_per_time_step_head)

        # with open(path_to_metadata_file, "w") as f:
        #     f.writelines(content_of_metadata_file)


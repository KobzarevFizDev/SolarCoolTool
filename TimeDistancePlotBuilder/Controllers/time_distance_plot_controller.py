from typing import TYPE_CHECKING

import os

from TimeDistancePlotBuilder.Models.app_models import AppModel, TimeDistancePlot, TDP
from TimeDistancePlotBuilder.Views.time_distance_plot_view import TimeDistancePlotView

from PyQt5.QtGui import QPixmap

if TYPE_CHECKING:
    from TimeDistancePlotBuilder.Models.app_models import Cubedata

class TimeDistancePlotController:
    def __init__(self, model, mainAppWindow):
        self.__model: AppModel = model
        self.__view: TimeDistancePlotView = TimeDistancePlotView(self, model, mainAppWindow)


    def set_current_tdp_step(self, step: int) -> None:
        self.__model.time_line.tdp_step = step
        self.__model.notify_observers()

    def set_smooth_parametr(self, smooth_parametr_slider_value: int) -> None:
        smooth_parametr_value = smooth_parametr_slider_value / 100

    def set_range_of_tdp_build(self, range) -> None:
        start_frame_index: int = range[0]
        finish_frame_index: int = range[1]

    def build_time_distance_plot(self) -> None:
        start_index: int = self.__model.time_line.start_frame_to_build_tdp
        finish_index: int = self.__model.time_line.finish_interval_of_time_distance_plot
        cubedata: Cubedata = self.__model.solar_frames_storage.get_cubedata_by_interval(start_index, finish_index)
        channel: int = self.__model.current_channel.channel
        self.__model.time_distance_plot.build_test_tdp(300)
        # self.__model.time_distance_plot.build(cubedata, channel)
        current_tdp_step: int = self.__model.time_line.tdp_step
        pixmap: QPixmap = self.__model.time_distance_plot.convert_to_qpixmap(current_tdp_step, vertical_size_in_px=450, horizontal_viewport_size_in_px=570)
        self.__view.set_time_distance_plot_pixmap(pixmap)

    def debug_build_time_distance_plot(self) -> None:
        number_of_frames = self.__model.time_line.max_index_of_solar_frame_for_debug_tdp
        self.__model.time_distance_plot.build_test_tdp(number_of_frames)
        current_tdp_step: int = self.__model.time_line.tdp_step
        pixmap: QPixmap = self.__model.time_distance_plot.convert_to_qpixmap(current_tdp_step, vertical_size_in_px=450, horizontal_viewport_size_in_px=570)
        self.__view.set_time_distance_plot_pixmap(pixmap)
        self.__view.set_ranges_of_tdp_slider(number_of_frames)

    def export_time_distance_plot(self) -> None:
        path_to_dir_to_export_result = self.__create_dir_to_save_export_data()
        self.__export_time_distance_plot_as_png(path_to_dir_to_export_result)
        self.__export_time_distance_plot_as_numpy_array(path_to_dir_to_export_result)
        self.__export_metadata_of_time_distance_plot_as_txt_file(path_to_dir_to_export_result)

    def __create_dir_to_save_export_data(self) -> str:
        all_result_dirs = [d for d in os.listdir(self.__model.path_to_export_result) if os.path.isdir(os.path.join(self.__model.path_to_export_result, d))]
        result_dirs = [d for d in all_result_dirs if "result" in d]
        new_result_index = len(result_dirs) + 1
        name_of_dir_for_save_export_data = f"result {new_result_index}"
        path_to_dir_to_export_result = os.path.join(self.__model.path_to_export_result, name_of_dir_for_save_export_data)
        os.mkdir(path_to_dir_to_export_result)
        return path_to_dir_to_export_result

    def __export_time_distance_plot_as_png(self, path_of_dir_to_export_result: str) -> None:
        current_channel: int = self.__model.current_channel.channel
        path_to_save_time_distance_plot_as_png = os.path.join(path_of_dir_to_export_result, f"time_distance_plot_A{current_channel}.png")
        self.__time_distance_plot.save_as_png(path_to_save_time_distance_plot_as_png, current_channel)

    def __export_time_distance_plot_as_numpy_array(self, path_of_dir_to_export_result: str) -> None:
        current_channel: int = self.__model.current_channel.channel
        numpy_array_file_name = f"tdp_A{current_channel}.npy"
        path_to_save_time_distance_plot_as_numpy_array = os.path.join(path_of_dir_to_export_result, numpy_array_file_name)
        self.__time_distance_plot.save_numpy_array(path_to_save_time_distance_plot_as_numpy_array)

    def __export_metadata_of_time_distance_plot_as_txt_file(self, path_of_dir_to_export_result: str) -> None:
        current_channel: int = self.__model.current_channel.channel
        metadata_file_name = f"tdp_A{current_channel}_metadata.txt"
        path_to_metadata_file = os.path.join(path_of_dir_to_export_result, metadata_file_name)

        content_of_metadata_file = []
        number_of_slice_along_loop_head = "NUMBER_OF_SLICE_ALONG_LOOP=200 \n"
        number_of_segments_bezier_curve_head = "NUMBER_OF_SEGMENTS_BEZIER_CURVE=10 \n"
        channel_head = f"CHANNEL={current_channel} \n"
        number_of_pixels_per_time_step_head = "NUMBER_OF_PIXELS_PER_TIME_STEP=3 \n"

        content_of_metadata_file.append(number_of_slice_along_loop_head)
        content_of_metadata_file.append(number_of_segments_bezier_curve_head)
        content_of_metadata_file.append(channel_head)
        content_of_metadata_file.append(number_of_pixels_per_time_step_head)

        with open(path_to_metadata_file, "w") as f:
            f.writelines(content_of_metadata_file)


    def __create_time_distance_plot(self) -> None:
        start_index: int = self.__model.time_line.start_frame_to_build_tdp
        finish_index: int = self.__model.time_line.finish_interval_of_time_distance_plot
        bezier_mask = self.__model.bezier_mask
        viewport_transform = self.__model.viewport_transform
        cubedata: Cubedata = self.__model.solar_frames_storage.get_cubedata_by_interval(start_index, finish_index)
        time_distance_plot: TimeDistancePlot = TimeDistancePlot.create_distance_plot_from_real_data(bezier_mask, viewport_transform, cubedata)
        channel: int = self.__model.current_channel.channel
        pixmap = time_distance_plot.get_time_distance_plot_as_qpixmap_using_cmap_of_channel(channel)
        self.__view.set_time_distance_plot_pixmap(pixmap)


        # start_index: int = self.model.time_line.start_interval_of_time_distance_plot
        # finish_index: int = self.model.time_line.finish_interval_of_time_distance_plot
        # bezier_mask = self.model.bezier_mask
        # viewport_transform = self.model.viewport_transform
        # cubedata: Cubedata = self.model.solar_frames_storage.get_cubedata_by_interval(start_index, finish_index)
        # self.__time_distance_plot: TimeDistancePlot = TimeDistancePlot.create_distance_plot_from_real_data(bezier_mask,
        #                                                                                                    viewport_transform,
        #                                                                                                    cubedata)
        # channel: int = self.model.current_channel.channel
        # pixmap = self.__time_distance_plot.get_time_distance_plot_as_qpixmap_using_cmap_of_channel(channel)
        # self.view.update_time_distance_plot_pixmap(pixmap)
from typing import List, TYPE_CHECKING

import sunpy.visualization.colormaps.cm

if TYPE_CHECKING:
    from Models.app_models import AppModel, BezierMask, ViewportTransform, SolarFramesStorage

from PyQt5.QtCore import QPoint
from dda import get_pixels_of_line
import numpy.typing as npt
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os


class CubeData:
    def __init__(self, x_size_of_frame: int,
                 y_size_of_frame: int,
                 number_of_frames: int):
        self.__x_size_of_frame = x_size_of_frame
        self.__y_size_of_frame = y_size_of_frame
        self.__number_of_frames = number_of_frames
        self.__data: List[npt.NDArray] = [None] * self.__number_of_frames

    @property
    def x_size_of_frame(self) -> int:
        return self.__x_size_of_frame

    @property
    def y_size_of_frame(self) -> int:
        return self.__y_size_of_frame

    @property
    def number_of_frames(self) -> int:
        return self.__number_of_frames

    def set_frame(self, frame_like_array: npt.NDArray, index: int) -> None:
        print(f"create cubedata = {index}/{self.__number_of_frames-1}")
        self.__data[index] = frame_like_array

    # todo: Проверка на выход за пределы массива
    def get_frame(self, index: int) -> npt.NDArray:
        return self.__data[index]

    """
    def create_time_distance_plot(self) -> None:
        cm = sunpy.visualization.colormaps.cm.sdoaia211
        plt.imshow(self.__data[0].astype(np.float32), cmap=cm)
        plt.colorbar()
        plt.show()
    """

    def save_to(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

class TimeDistancePlot:
    def __init__(self, cubedata: CubeData, channel: int):
        self.__cubedata: CubeData = cubedata
        self.__channel = channel
        Ny = self.__cubedata.y_size_of_frame
        Nx = self.__cubedata.number_of_frames
        N = Nx * Ny
        self.__plot: npt.NDArray = np.arange(N).reshape(Ny, Nx)
        self.__create_plot()

    def show(self) -> None:
        cm = {94: sunpy.visualization.colormaps.cm.sdoaia94,
              131: sunpy.visualization.colormaps.cm.sdoaia131,
              171: sunpy.visualization.colormaps.cm.sdoaia171,
              193: sunpy.visualization.colormaps.cm.sdoaia193,
              211: sunpy.visualization.colormaps.cm.sdoaia211,
              304: sunpy.visualization.colormaps.cm.sdoaia304,
              355: sunpy.visualization.colormaps.cm.sdoaia335}[self.__channel]

        plt.imshow(self.__plot.astype(np.float32), cmap=cm)
        plt.colorbar()
        plt.show()

    def __create_plot(self) -> None:
        number_of_frames = self.__cubedata.number_of_frames
        for i in range(number_of_frames):
            midline = self.__get_midline_of_frame_with_index(i)
            self.__plot.T[i] = midline
        print(self.__plot)

    def __get_midline_of_frame_with_index(self, index_of_frame: int) -> npt.NDArray:
        y = int(self.__cubedata.y_size_of_frame / 2)
        frame = self.__cubedata.get_frame(index_of_frame)
        return frame.T[y]

class MaskExporter:
    def __init__(self, solar_frames_storage: 'SolarFramesStorage',
                 viewport_transform: 'ViewportTransform',
                 bezier_mask: 'BezierMask'):
        self.__solar_frames_storage: SolarFramesStorage = solar_frames_storage
        self.__bezier_mask: BezierMask = bezier_mask
        self.__viewport_transform: ViewportTransform = viewport_transform
        self.__pixels_of_mask: List[QPoint] = list()
        self.__mask_width: int = 10_000
        self.__mask_length: int = 0

        self.__cubedata_for_a94: CubeData = None
        self.__cubedata_for_a131: CubeData = None
        self.__cubedata_for_a171: CubeData = None
        self.__cubedata_for_a193: CubeData = None
        self.__cubedata_for_a211: CubeData = None
        self.__cubedata_for_a355: CubeData = None

    def __create_2darray(self, x_size: int, y_size: int) -> npt.NDArray:
        return np.arange(x_size * y_size).reshape(y_size, x_size)

    def __get_value_of_mask_pixels_for_frame(self, channel: int, index: int) -> npt.NDArray:
        solar_frame = (self.__solar_frames_storage
                       .get_solar_frame_by_index_from_channel(channel, index))

        value_of_mask_pixels_for_this_frame = self.__create_2darray(self.__mask_length, self.__mask_width)

        i = 0
        for y in range(self.__mask_width):
            for x in range(self.__mask_length):
                pixel = self.__pixels_of_mask[i]
                pixel_value = solar_frame.pixels_array[pixel.y()][pixel.x()]
                value_of_mask_pixels_for_this_frame[y][x] = pixel_value
                i += 1
        return value_of_mask_pixels_for_this_frame

    def __getcube_data_for_channel(self, channel: int) -> CubeData:
        number_of_solar_frames_for_this_channel = self.__solar_frames_storage.get_number_of_frames_in_channel(channel)
        cube_data = CubeData(self.__mask_length, self.__mask_width, number_of_solar_frames_for_this_channel)
        for index_of_frame in range(number_of_solar_frames_for_this_channel):
            pixels_values = self.__get_value_of_mask_pixels_for_frame(channel, index_of_frame)
            cube_data.set_frame(pixels_values, index_of_frame)
        return cube_data

    def __initialize_size_of_mask(self, number_of_sections: int) -> None:
        self.__mask_length = number_of_sections
        top_border = self.__bezier_mask.get_top_border(number_of_sections)
        bottom_border = self.__bezier_mask.get_bottom_border(number_of_sections)
        for x in range(number_of_sections):
            top_point_in_view: QPoint = top_border[x]
            bottom_point_in_view: QPoint = bottom_border[x]
            top_point_in_image = (self.__viewport_transform
                                  .transform_from_viewport_pixel_to_image_pixel(top_point_in_view))
            bottom_point_in_image = (self.__viewport_transform
                                     .transform_from_viewport_pixel_to_image_pixel(bottom_point_in_view))

            pixels_in_image_of_current_section = get_pixels_of_line(top_point_in_image.x(),
                                                                    top_point_in_image.y(),
                                                                    bottom_point_in_image.x(),
                                                                    bottom_point_in_image.y())

            if self.__mask_width > len(pixels_in_image_of_current_section):
                self.__mask_width = len(pixels_in_image_of_current_section)



    def transform_to_rectangle_use_cross_section(self, number_of_sections: int) -> 'MaskExporter':
        self.__initialize_size_of_mask(number_of_sections)
        top_border = self.__bezier_mask.get_top_border(number_of_sections)
        bottom_border = self.__bezier_mask.get_bottom_border(number_of_sections)
        for x in range(number_of_sections):
            top_point_in_view: QPoint = top_border[x]
            bottom_point_in_view: QPoint = bottom_border[x]
            top_point_in_image = (self.__viewport_transform
                                  .transform_from_viewport_pixel_to_image_pixel(top_point_in_view))
            bottom_point_in_image = (self.__viewport_transform
                                     .transform_from_viewport_pixel_to_image_pixel(bottom_point_in_view))

            pixels_in_image_of_current_section = get_pixels_of_line(top_point_in_image.x(),
                                                   top_point_in_image.y(),
                                                   bottom_point_in_image.x(),
                                                   bottom_point_in_image.y())

            for y in range(self.__mask_width):
                self.__pixels_of_mask.append(pixels_in_image_of_current_section[y])

        return self

    def is_possible_export_cubedata_for_channel(self, channel: int) -> bool:
        return self.__solar_frames_storage.is_exist_solar_frames_in_channel(channel)

    def export_cubedata_for_channel(self, channel: int) -> CubeData:
        return self.__getcube_data_for_channel(channel)


class SaverResults:
    def __init__(self, app_model: 'AppModel', path_to_export: str):
        self.__app_model: AppModel = app_model
        self.__path_to_export = path_to_export

    def save_result(self):
        frames_storage = self.__app_model.solar_frames_storage
        viewport_transform = self.__app_model.viewport_transform
        bezier_mask = self.__app_model.bezier_mask
        mask_exporter = MaskExporter(frames_storage, viewport_transform, bezier_mask)
        mask_exporter.transform_to_rectangle_use_cross_section(100)

        self.__save_cube_data_for_channel(mask_exporter, self.__app_model.current_channel.channel)

        # todo: для всех каналов

    def create_time_distance_plot_for_saved_data_if_possible(self):
        if self.__is_exist_saved_cubedata_for_channel(211):
            cube_data_a211 = self.__load_cubedata_for_channel(211)
            time_distance_plot = TimeDistancePlot(cube_data_a211, 211)
            time_distance_plot.show()
        else:
            print("Not found saved cube data for channel A94")


    def __save_cube_data_for_channel(self, mask_exporter: MaskExporter, channel: int) -> None:
        if mask_exporter.is_possible_export_cubedata_for_channel(channel):
            cube_data_a94: CubeData = mask_exporter.export_cubedata_for_channel(channel)
            path_to_save = self.__get_path_to_cubedata_for_channel(channel)
            cube_data_a94.save_to(path_to_save)
            print(f"Saved cubedata for channel {channel}")

    def __is_exist_saved_cubedata_for_channel(self, channel: int) -> bool:
        path_to_cubedata = self.__get_path_to_cubedata_for_channel(channel)
        return os.path.isfile(path_to_cubedata)

    def __get_path_to_cubedata_for_channel(self, channel: int) -> str:
        return self.__path_to_export + f"\\cube_data_a{channel}.cubedata"

    def __load_cubedata_for_channel(self, channel: int) -> CubeData:
        path_to_cubedata = self.__get_path_to_cubedata_for_channel(channel)
        with open(path_to_cubedata, "rb") as f:
            return pickle.load(f)

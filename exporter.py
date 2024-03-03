from typing import List

from PyQt5.QtCore import QPoint
from Models.app_models import AppModel, BezierMask, ViewportTransform, SolarFramesStorage, SolarFrame
from dda import get_pixels_of_line
import numpy.typing as npt
import numpy as np


class CubeData:
    def __init__(self, x_size_of_frame: int,
                 y_size_of_frame: int,
                 number_of_frames: int):
        self.__x_size_of_frame = x_size_of_frame
        self.__y_size_of_frame = y_size_of_frame
        self.__number_of_frame = number_of_frames
        self.__data: List[npt.NDArray] = list()

    def set_frame(self, frame_like_array: npt.NDArray, index: int) -> None:
        self.__data[index] = frame_like_array


class MaskExporter:
    def __init__(self, solar_frames_storage: SolarFramesStorage,
                 viewport_transform: ViewportTransform,
                 bezier_mask: BezierMask):
        self.__solar_frames_storage = solar_frames_storage
        self.__bezier_mask: BezierMask = bezier_mask
        self.__viewport_transform: ViewportTransform = viewport_transform
        self.__pixels_of_mask: npt.NDArray = None

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

        y_size = self.__pixels_of_mask.shape[0]
        x_size = self.__pixels_of_mask.shape[1]

        value_of_mask_pixels_for_this_frame = self.__create_2darray(x_size, y_size)

        for y in range(y_size):
            for x in range(x_size):
                pixel = self.__pixels_of_mask[y][x]
                pixel_value = solar_frame.pixels_array[pixel.y()][pixel.x()]
                value_of_mask_pixels_for_this_frame[y][x] = pixel_value
        return value_of_mask_pixels_for_this_frame

    def __get_cube_data_for_channel(self, channel: int) -> CubeData:
        cube_data = None
        number_of_solar_frames_for_this_channel = self.__solar_frames_storage.get_number_of_frames_in_channel(channel)
        for index_of_frame in range(number_of_solar_frames_for_this_channel):
            pixels_values = self.__get_value_of_mask_pixels_for_frame(channel, index_of_frame)
            y_size_of_frame = pixels_values.shape[0]
            x_size_of_frame = pixels_values.shape[1]
            cube_data = CubeData(x_size_of_frame, y_size_of_frame, number_of_solar_frames_for_this_channel)
        return cube_data

    def transform_to_rectangle_use_cross_section(self, number_of_sections: int) -> 'MaskExporter':
        self.__pixels_of_mask = self.__create_2darray(number_of_sections, self.__bezier_mask.width_in_pixels)

        top_border = self.__bezier_mask.get_top_border()
        bottom_border = self.__bezier_mask.get_bottom_border()
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

            for y in range(len(pixels_in_image_of_current_section)):
                self.__pixels_of_mask[y][x] = pixels_in_image_of_current_section[y]
        return self


    def export_for_a94_if_possible(self) -> 'MaskTransform':
        if self.__solar_frames_storage.is_exist_solar_frames_in_channel(94):
            self.__cubedata_for_a94 = self.__get_cube_data_for_channel(94)
            return self
        else:
            return self

    def export_for_a131_if_possible(self) -> 'MaskTransform':
        if self.__solar_frames_storage.is_exist_solar_frames_in_channel(131):
            self.__cubedata_for_a131 = self.__get_cube_data_for_channel(131)
            return self
        else:
            return self

    def export_for_a171_if_possible(self) -> 'MaskTransform':
        if self.__solar_frames_storage.is_exist_solar_frames_in_channel(171):
            self.__cubedata_for_a171 = self.__get_cube_data_for_channel(171)
            return self
        else:
            return self

    def save(self) -> None:
        pass

class Exporter:
    def __init__(self, app_model: AppModel, path_to_export: str):
        self.__app_model = app_model
        self.__path_to_export = path_to_export

    def export_result(self):
        frames_storage = self.__app_model.solar_frames_storage
        viewport_transform = self.__app_model.viewport_transform
        bezier_mask = self.__app_model.bezier_mask
        mask_exporter = MaskExporter(frames_storage, viewport_transform, bezier_mask)

        (mask_exporter
         .transform_to_rectangle_use_cross_section(100)
         .export_for_a94_if_possible()
         .export_for_a131_if_possible())

import math
import os
import sqlite3
from typing import List
from enum import IntEnum, unique

from matplotlib import pyplot as plt

from TimeDistancePlotBuilder.dda import get_pixels_of_line, get_pixels_of_cicle
from scipy.ndimage import zoom, gaussian_filter

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure, SubplotParams

import numpy as np
from PyQt5.QtCore import QPoint, QRect
import sunpy.map
import sunpy.data.sample
import sunpy.visualization.colormaps.cm
from PyQt5.QtGui import QImage, QPixmap
from astropy.io import fits
import numpy.typing as npt

from TimeDistancePlotBuilder import transformations

from TimeDistancePlotBuilder.configuration import ConfigurationApp

from aiapy.calibrate import normalize_exposure, register, update_pointing


def get_cmap_by_channel(channel: int):
    if channel not in [94, 131, 171, 193, 211, 304, 335]:
        raise Exception(
            f"TimeDistancePlot::get_time_distance_plot_as_qpixmap_using_cmap_of_channel({channel}). Not correct channel")

    cm = {94: sunpy.visualization.colormaps.cm.sdoaia94,
          131: sunpy.visualization.colormaps.cm.sdoaia131,
          171: sunpy.visualization.colormaps.cm.sdoaia171,
          193: sunpy.visualization.colormaps.cm.sdoaia193,
          211: sunpy.visualization.colormaps.cm.sdoaia211,
          304: sunpy.visualization.colormaps.cm.sdoaia304,
          335: sunpy.visualization.colormaps.cm.sdoaia335
          }[channel]
    return cm


class CubedataFrame:
    def __init__(self, content: npt.NDArray):
        self.__frame_content: npt.NDArray = content
        self.__start_border_of_line: int = -1
        self.__finish_border_of_line: int = -1

    def set_border_of_time_distance_plot_line(self, start_border: int, finish_border: int) -> None:
        self.__start_border_of_line = start_border
        self.__finish_border_of_line = finish_border


    @property
    def frame_content(self) -> npt.NDArray:
        return self.__frame_content

    @property
    def width_of_frame(self) -> int:
        return self.__frame_content.shape[1]

    @property
    def height_of_frame(self) -> int:
        return self.__frame_content.shape[0]

    @property
    def start_border_of_line(self) -> int:
        return self.__start_border_of_line

    @property
    def finish_border_of_line(self) -> int:
        return self.__finish_border_of_line


class Cubedata:
    def __init__(self, x_size: int, y_size: int):
        self.__x_size = x_size
        self.__y_size = y_size
        self.__frames: List[CubedataFrame] = list()

    def add_frame(self, frame: CubedataFrame):
        if not frame.width_of_frame == self.__y_size:
            raise Exception(f"Dont match y size of cubedata and frame. [{frame.shape[1]}] [{self.__y_size}]")

        if not frame.height_of_frame == self.__x_size:
            raise Exception(f"Dont match x size of cubedata and frame. [{frame.shape[0]}] [{self.__x_size}]")

        self.__frames.append(frame)

    @property
    def number_of_frames(self) -> int:
        return len(self.__frames)

    def get_frame(self, index: int) -> CubedataFrame:
        if index >= len(self.__frames):
            raise Exception("CubeData::get_frame() index out")
        return self.__frames[index]

    @classmethod
    def create_from_debug_data(cls, number_of_frames: int):
        cubedata = cls(600, 600)
        animated_frame = TestAnimatedFrame("horizontal", 30, 600)
        number_of_steps = 100
        t_values = [i/number_of_steps for i in range(number_of_frames)]
        for t in t_values:
            frame = animated_frame.get_frame_by_t(t)
            cubedata.add_frame(frame)
        return cubedata


class TestAnimatedFrame:
    def __init__(self,
                 direction: str,
                 width_line: int,
                 size: int):
        self.__direction = direction
        self.__width_line = width_line
        self.__size = size
        self.__t = 0
        self.__frame = self.get_frame_by_t(0)


    @property
    def current_t(self) -> float:
        return self.__t

    @current_t.setter
    def current_t(self, value) -> None:
        self.__t = self.__validate_t_value(value)

    def animate_frame(self, delta_t: float):
        self.__t += delta_t
        self.__t = self.__validate_t_value(self.__t)
        self.__frame = self.__create_content_frame()
        self.__draw_line(self.__t, self.__frame)

    def get_frame_by_t(self, t: float) -> CubedataFrame:
        t = self.__validate_t_value(t)
        content_frame = self.__create_content_frame()
        start_border, finish_border = self.__draw_line(t, content_frame)
        frame = CubedataFrame(content_frame)
        frame.set_border_of_time_distance_plot_line(start_border, finish_border)
        return frame

    def get_frame_by_t_as_qpixmap(self, t: float) -> QPixmap:
        frame_content = self.get_frame_by_t(t).frame_content
        frame_content = frame_content.astype(np.uint8)
        qimage = QImage(frame_content, self.__size, self.__size, self.__size, QImage.Format_Grayscale8)
        return QPixmap.fromImage(qimage)

    def __validate_t_value(self, t: float) -> float:
        if t < 0:
            return 0
        elif t > 1:
            return 1
        else:
            return t

    def __draw_line(self, t, frame):
        if self.__direction == "horizontal":
            return self.__draw_horizontal_line(t, frame)
        elif self.__direction == "vertical":
            return self.__draw_vertical_line(t, frame)

    def __draw_horizontal_line(self, t, frame):
        start_border, end_border = self.__get_line_border_of_line(t)

        for i in range(start_border, end_border):
            frame[i] = 0

        return start_border, end_border

    def __draw_vertical_line(self, t, frame):
        start_border, end_border = self.__get_line_border_of_line(t)
        for i in range(start_border, end_border):
            frame.T[i] = 0

    def __create_content_frame(self):
        return np.ones((self.__size, self.__size)) * 255

    def __get_line_border_of_line(self, t: float) -> [int, int]:
        line_position = self.__get_line_pixel_position(t)
        start_border = int(line_position - self.__width_line / 2)
        end_border = int(line_position + self.__width_line / 2)

        if start_border < 0:
            start_border = 0

        if end_border > self.__size:
            end_border = self.__size

        return start_border, end_border

    def __get_line_pixel_position(self, t: float) -> int:
        return int(self.__lininterp(0, self.__size, t))

    def __lininterp(self, p0: int, p1: int, t: float) -> float:
        return (1 - t) * p0 + t * p1


class SolarFrame:
    def __init__(self,
                 id: int,
                 path_to_fits_file: str,
                 channel: int,
                 date: str):
        self.__id: int = id
        self.__path_to_fits_file: str = path_to_fits_file
        self.__channel: int = channel
        self.__date: str = date
        self.__map = self.__get_map()
        self.__pixels_array: npt.NDArray = self.__get_pixels_array()
        self.__qimage = self.__get_qtimage()
        self.__viewport_transform: ViewportTransform = None


    @property
    def id(self) -> int:
        return self.__id

    @property
    def channel(self) -> int:
        return self.__channel

    @property
    def pixels_array(self) -> npt.NDArray:
        return self.__pixels_array

    @property
    def qtimage(self) -> QImage:
        return self.__qimage

    def set_viewport_transform(self, viewport_transform: 'ViewportTransform') -> None:
        self.__viewport_transform = viewport_transform

    def get_pixmap_of_solar_region(self,
                                   top_left_in_view: QPoint,
                                   bottom_right_in_view: QPoint) -> QPixmap:
        top_left_in_image = (self.__viewport_transform
                             .transform_from_viewport_pixel_to_image_pixel(top_left_in_view))
        bottom_right_in_image = (self.__viewport_transform
                                 .transform_from_viewport_pixel_to_image_pixel(bottom_right_in_view))
        rect = QRect(top_left_in_image, bottom_right_in_image)
        pixmap_from_origin_frame = QPixmap.fromImage(self.__qimage.copy(rect))
        scaled_pixmap_of_frame = pixmap_from_origin_frame.scaled(600, 600)
        return scaled_pixmap_of_frame

    def __get_pixels_array(self) -> npt.NDArray:
        return self.__map.data

    def __get_map(self):
        m = sunpy.map.Map(self.__path_to_fits_file)
        return m


    def __get_qtimage(self) -> QImage:
        sp = SubplotParams(left=0., bottom=0., right=1., top=1.)
        fig = Figure((40.96, 40.96), subplotpars=sp)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(projection=self.__map)
        self.__map.plot(axes=ax)
        ax.set_axis_off()
        canvas.draw()
        width, height = fig.figbbox.width, fig.figbbox.height
        im = QImage(canvas.buffer_rgba(), int(width), int(height), QImage.Format_RGBA8888)
        return im

# todo: Валидацию на корректное значение channel
class SolarFramesStorage:
    def __init__(self, viewport_transform: 'ViewportTransform', configuration_app: 'ConfigurationApp'):
        self.__viewport_transform = viewport_transform
        self.__configuration_app: 'ConfigurationApp' = configuration_app
        self.__current_channel: int = configuration_app.initial_channel
        self.__path_to_directory: str = configuration_app.path_to_solar_images
        self.__loaded_channel: List[SolarFrame] = list()
        self.__initialize_database()
        self.cache_channel(configuration_app.initial_channel)

    def __initialize_database(self) -> None:
        files = self.__get_files_in_directory()
        channels = self.__get_channels(files)
        dates = self.__get_dates_of_this_files(files)

        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS Images")
        cursor.execute("""
        CREATE TABLE Images(
        Id INTEGER PRIMARY KEY,
        Path TEXT NOT NULL,
        Channel INTEGER NOT NULL,
        Date TEXT NOT NULL
        )
        """)
        for i, file in enumerate(files):
            insert_command = "INSERT INTO Images (Id, Path, Channel, Date) VALUES (?,?,?,?)"
            insert_data = (i, file, channels[i], dates[i])
            cursor.execute(insert_command, insert_data)
        connection.commit()
        connection.close()

    def __get_files_in_directory(self) -> List[str]:
        files_in_directory = []
        for root, dirs, files in os.walk(self.__path_to_directory):
            for file in files:
                files_in_directory.append(os.path.join(root, file))
        files_in_directory = list(filter((lambda f: "image" in f), files_in_directory))
        return files_in_directory


    def __get_channels(self, files) -> List[int]:
        return [f.split('.')[3] for f in files]

    def __get_dates_of_this_files(self, files) -> List[str]:
        return [f.split('.')[2][0:10] for f in files]

    # todo: Дублирование кода с методом __load_channel
    def cache_channel(self, channel: int) -> None:
        step = self.__configuration_app.get_step_for_channel(channel)
        limit = self.__configuration_app.get_limit_for_channel(channel)
        need_to_skip = step - 1
        cached_frames = 0

        self.__current_channel = channel
        self.__loaded_channel.clear()

        files = self.__get_files_in_channel(channel)
        ids = self.__get_ids_of_frames_in_channel(channel)
        dates = self.__get_dates_of_files_in_channel(channel)

        for i, path in enumerate(files):
            if cached_frames > limit:
                print("Acheve limit")
                break
            print(f"caching {cached_frames}/{len(files)}. i = {i}")

            if need_to_skip > 0:
                print(f"skip {i}")
                need_to_skip -= 1
                continue

            cached_frames += 1
            id = ids[i]
            date = dates[i]
            solar_frame = SolarFrame(id, path, channel, date)
            solar_frame.set_viewport_transform(self.__viewport_transform)

            self.__loaded_channel.append(solar_frame)

            need_to_skip = step - 1

    # todo: Валидация параметров
    def get_solar_frame_by_index_from_current_channel(self, index: int) -> SolarFrame:
        res = self.__loaded_channel[index]
        return res

    def get_number_of_frames_in_current_channel(self) -> int:
        return len(self.__loaded_channel)

    def __get_number_of_frames_of_channel_in_database(self, channel: int) -> int:
        connection = sqlite3.connect("my_database.db")
        cursor = connection.cursor()
        command = "SELECT COUNT(*) FROM Images WHERE Channel = {0}".format(channel)
        number_of_images = int(cursor.execute(command).fetchall()[0][0])
        connection.close()
        return number_of_images
    
    def is_exist_solar_frames_in_channel(self, channel: int) -> bool:
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(channel)
        frames = cursor.execute(command).fetchall()
        connection.close()
        return len(frames) > 0
    
    def is_exist_solar_frames_in_current_channel(self) -> bool:
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(self.__current_channel)
        frames = cursor.execute(command).fetchall()
        connection.close()
        return len(frames) > 0

    def __get_ids_of_frames_in_channel(self, channel: int) -> List[int]:
        connection = sqlite3.connect("my_database.db")
        cursor = connection.cursor()
        command = "SELECT Id FROM Images WHERE Channel = {0}".format(channel)
        ids = cursor.execute(command).fetchall()
        ids = [ids[i][0] for i in range(len(ids))]
        connection.close()
        return ids

    def __get_files_in_channel(self, channel: int) -> List[str]:
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(channel)
        paths_to_files = cursor.execute(command).fetchall()
        paths_to_files = [paths_to_files[i][0] for i in range(len(paths_to_files))]
        connection.close()
        return paths_to_files

    def __get_dates_of_files_in_channel(self, channel: int) -> List[str]:
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        command = "SELECT Date FROM Images WHERE Channel = {0}".format(channel)
        dates = cursor.execute(command).fetchall()
        dates = [dates[i][0] for i in range(len(dates))]
        connection.close()
        return dates

    # t = 0 <-> 1
    def get_cubedata_by_interval(self, start_index: int, finish_index) -> Cubedata:
        first_frame = self.get_solar_frame_by_index_from_current_channel(start_index)
        x_size = first_frame.pixels_array.shape[1]
        y_size = first_frame.pixels_array.shape[0]
        cubedata = Cubedata(x_size, y_size)
        for index in range(start_index, finish_index):
            solar_frame: SolarFrame = self.get_solar_frame_by_index_from_current_channel(index)
            content = solar_frame.pixels_array
            frame = CubedataFrame(content)
            cubedata.add_frame(frame)
        return cubedata


class BezierCurve:
    def __init__(self,
                 p0: QPoint,
                 p1: QPoint,
                 p2: QPoint,
                 p3: QPoint):
        self.__p0: QPoint = p0
        self.__p1: QPoint = p1
        self.__p2: QPoint = p2
        self.__p3: QPoint = p3

    @property
    def points(self) -> List[QPoint]:
        return [self.__p0, self.__p1, self.__p2, self.__p3]

    def point_at_t(self, t) -> QPoint:
        A = (1-t)**3 * self.__p0
        B = 3 * (1-t)**2 * t * self.__p1
        C = 3 * (1-t)*t**2 * self.__p2
        D = t**3 * self.__p3

        return A + B + C + D

    def tangent_at_t(self, t) -> QPoint:
        A = 3 * (1-t)**2 * (self.__p1 - self.__p0)
        B = 6 * (1 - t) * t * (self.__p2 - self.__p1)
        C = 3 * t**2 * (self.__p3 - self.__p2)
        return A + B + C

    def normal_at_t(self, t) -> QPoint:
        tangent = self.tangent_at_t(t)
        return QPoint(tangent.y(), -tangent.x())

# todo: Написать тесты для проверки границ маски

class BezierMask:
    def __init__(self,
                 number_of_segments=10,
                 width_in_pixels=30,
                 min_number_of_segments=3,
                 max_number_of_segments=100):
        self.__number_of_segments: int = number_of_segments
        self.__width_in_pixels: int = width_in_pixels
        self.__min_number_of_segments: int = min_number_of_segments
        self.__max_number_of_segments: int = max_number_of_segments
        self.__bezier_curve: BezierCurve = self.__create_initial_bezier_curve()

    @property
    def width_in_pixels(self) -> int:
        return self.__width_in_pixels

    @property
    def bezier_curve(self) -> BezierCurve:
        return self.__bezier_curve

    @property
    def number_of_segments(self) -> int:
        return self.__number_of_segments

    def __create_initial_bezier_curve(self) -> BezierCurve:
        bezier_curve = BezierCurve(QPoint(100, 100),
                                   QPoint(200, 200),
                                   QPoint(300, 150),
                                   QPoint(400, 300))
        return bezier_curve

    def get_top_border(self, number_of_segments=-1) -> List[QPoint]:
        number_of_segments = self.__number_of_segments if number_of_segments == -1 else number_of_segments
        border_points: List[QPoint] = list()
        for i in range(number_of_segments + 1):
            t = i / number_of_segments
            normal_at_t: QPoint = self.__bezier_curve.normal_at_t(t)
            point_at_t: QPoint = self.__bezier_curve.point_at_t(t)
            magnitude_of_normal = math.sqrt(normal_at_t.x() ** 2 + normal_at_t.y() ** 2)
            border_point = point_at_t + QPoint(int(self.__width_in_pixels * normal_at_t.x() / magnitude_of_normal),
                                               int(self.__width_in_pixels * normal_at_t.y() / magnitude_of_normal))
            border_points.append(border_point)
        return border_points

    def get_bottom_border(self, number_of_segments=-1) -> List[QPoint]:
        number_of_segments = self.__number_of_segments if number_of_segments == -1 else number_of_segments
        border_points: List[QPoint] = list()
        for i in range(number_of_segments + 1):
            t = i / number_of_segments
            border_point = self.__bezier_curve.point_at_t(t)
            border_points.append(border_point)
        return border_points

    def increase_number_of_segments(self) -> None:
        self.__number_of_segments += 1
        if self.__number_of_segments > self.__max_number_of_segments:
            self.__number_of_segments = self.__max_number_of_segments

    def decrease_number_of_segments(self):
        self.__number_of_segments -= 1
        if self.__number_of_segments < self.__min_number_of_segments:
            self.__number_of_segments = self.__min_number_of_segments


# todo: присвоение начального канала является ошибкой, нужно также убиться что данный канал есть на диске
class CurrentChannel:
    def __init__(self, solar_frames_storage: SolarFramesStorage, initial_channel=94):
        self.__solar_frames_storage = solar_frames_storage
        self.__total_channels_of_sdo = [94, 131, 171, 193, 211, 355]
        self.__current_channel: int = initial_channel \
            if self.__is_this_channel_valid(initial_channel) \
            else self.__total_channels_of_sdo[0]
        self.__current_channel_was_changed: bool = False

    @property
    def available_channels(self) -> List[int]:
        available_channels_list = list()
        for channel in self.__total_channels_of_sdo:
            if self.__solar_frames_storage.is_exist_solar_frames_in_channel(channel):
                available_channels_list.append(channel)
        return available_channels_list

    @property
    def not_available_channels(self) -> List[int]:
        not_available_channels_list = list()
        for channel in self.__total_channels_of_sdo:
            if not self.__solar_frames_storage.is_exist_solar_frames_in_channel(channel):
                not_available_channels_list.append(channel)
        return not_available_channels_list

    @property
    def channel(self) -> int:
        return self.__current_channel

    @channel.setter
    def channel(self, new_channel) -> None:
        if self.__is_this_channel_valid(new_channel):
            self.__current_channel = new_channel
        else:
            raise Exception("This channel = {0} isn't correct".format(new_channel))

    @property
    def current_channel_was_changed(self) -> bool:
        res = self.__current_channel_was_changed
        self.__current_channel_was_changed = False
        return res

    @property
    def number_of_images_in_current_channel(self) -> int:
        channel = self.__current_channel
        return self.__solar_frames_storage.get_number_of_frames_in_current_channel()

    def __is_this_channel_valid(self, channel: int) -> bool:
        return channel in self.__total_channels_of_sdo


class InterestingSolarRegion:
    def __init__(self):
        self.__top_right_in_view: QPoint = QPoint(600, 0)
        self.__bottom_left_in_view: QPoint = QPoint(0, 600)

        self.__top_right_point_was_selected: bool = False
        self.__bottom_left_point_was_selected: bool = False

    @property
    def top_right_in_view(self) -> QPoint:
        if self.__top_right_point_was_selected:
            #self.__top_right_point_was_selected = False
            return self.__top_right_in_view
        else:
            raise Exception("Top right point was not selected")

    @property
    def top_left_in_view(self) -> QPoint:
        return QPoint(self.__bottom_left_in_view.x(), self.__top_right_in_view.y())

    @property
    def bottom_left_in_view(self) -> QPoint:
        if self.__bottom_left_point_was_selected:
            #self.__bottom_left_point_was_selected = False
            return self.__bottom_left_in_view
        else:
            raise Exception("Bottom left point was not selected")

    @property
    def bottom_right_in_view(self) -> QPoint:
        return QPoint(self.__top_right_in_view.x(), self.__bottom_left_in_view.y())

    def set_top_right_in_view(self, point: QPoint) -> None:
        self.__top_right_point_was_selected = True
        self.__top_right_in_view = point
        if self.__top_right_point_was_selected and self.__bottom_left_point_was_selected:
            self.__align_to_square_if_necessary()

    def set_bottom_left_in_view(self, point: QPoint) -> None:
        self.__bottom_left_point_was_selected = True
        self.__bottom_left_in_view = point
        if self.__top_right_point_was_selected and self.__bottom_left_point_was_selected:
            self.__align_to_square_if_necessary()

    def __align_to_square_if_necessary(self) -> None:
        x_side_size = self.__bottom_left_in_view.x() - self.__top_right_in_view.x()
        y_side_size = self.__top_right_in_view.y() - self.__bottom_left_in_view.y()
        side_size = (x_side_size + y_side_size)/2
        half_side_size = side_size/2
        center_of_square = QPoint(int((self.__top_right_in_view.x() + self.__bottom_left_in_view.x()) / 2),
                                  int((self.__top_right_in_view.y() + self.__bottom_left_in_view.y()) / 2))

        self.__top_right_in_view = QPoint(int(center_of_square.x() + half_side_size),
                                          int(center_of_square.y() + half_side_size))
        self.__bottom_left_in_view = QPoint(int(center_of_square.x() - half_side_size),
                                            int(center_of_square.y() - half_side_size))



# todo: Подумать над названием
class ViewportTransform:
    def __init__(self):
        self.__zoom = 1
        self.__origin_size_image = 600
        self.__offset: QPoint = QPoint(0, 0)

    @property
    def zoom(self) -> float:
        return self.__zoom

    @zoom.setter
    def zoom(self, new_zoom) -> None:
        if new_zoom < 0:
            raise Exception("Zoom cannot be negative")
        else:
            self.__zoom = new_zoom

    @property
    def offset(self) -> QPoint:
        return self.__offset

    @offset.setter
    def offset(self, new_offset) -> None:
        self.__offset = new_offset

    def transform_from_viewport_pixel_to_image_pixel(self, viewport_pixel: QPoint) -> QPoint:
        image_pixel = transformations.transform_point_from_view_to_image(viewport_pixel,
                                                                         [600, 600],
                                                                         [4096, 4096],
                                                                         self.__zoom,
                                                                         self.__offset)
        return image_pixel

    def transform_from_image_pixel_to_viewport_pixel(self, image_pixel: QPoint) -> QPoint:
        viewport_pixel = transformations.transform_point_from_image_to_view(image_pixel,
                                                                            [600, 600],
                                                                            [4096, 4096],
                                                                            self.__zoom,
                                                                            self.__offset)
        return viewport_pixel

    def get_transformed_pixmap_for_viewport(self, solar_frame: SolarFrame) -> QPixmap:
        scale: int = int(self.__zoom * self.__origin_size_image)
        scaled_solar_frame = solar_frame.qtimage.scaled(scale, scale)
        pixmap_for_draw = QPixmap.fromImage(scaled_solar_frame)
        return pixmap_for_draw


class TimeLine:
    def __init__(self, solar_frames_storage: SolarFramesStorage):
        self.__solar_frames_storage: SolarFramesStorage = solar_frames_storage
        self.__index_of_current_solar_frame: int = 0
        self.__start_interval_border_of_time_distance_plot: int = 0
        self.__finish_interval_border_of_time_distance_plot: int = 3

    @property
    def index_of_current_solar_frame(self) -> int:
        return self.__index_of_current_solar_frame

    @index_of_current_solar_frame.setter
    def index_of_current_solar_frame(self, new_index) -> None:
        number_of_solar_frames_in_current_channel = self.__solar_frames_storage.get_number_of_frames_in_current_channel()
        if new_index >= number_of_solar_frames_in_current_channel:
            raise Exception(f"Index of current solar frame cannot be >= number of solar frames in current channel. Index = {new_index}")

        self.__index_of_current_solar_frame = new_index

    @property
    def start_interval_of_time_distance_plot(self) -> int:
        return self.__start_interval_border_of_time_distance_plot

    @start_interval_of_time_distance_plot.setter
    def start_interval_of_time_distance_plot(self, new_index) -> None:
        number_of_solar_frames_in_current_channel = self.__solar_frames_storage.get_number_of_frames_in_current_channel()
        if new_index >= number_of_solar_frames_in_current_channel:
            raise Exception(f"Index of start interval time distance plot cannot be >= number of solar frames in current channel. Index = {new_index}")

        self.__start_interval_border_of_time_distance_plot = new_index

    @property
    def finish_interval_of_time_distance_plot(self) -> int:
        return self.__finish_interval_border_of_time_distance_plot

    @finish_interval_of_time_distance_plot.setter
    def finish_interval_of_time_distance_plot(self, new_index) -> None:
        number_of_solar_frames_in_current_channel = self.__solar_frames_storage.get_number_of_frames_in_current_channel()
        if new_index >= number_of_solar_frames_in_current_channel:
            raise Exception("Index of finish interval time distance plot cannot be >= number of solar frames in current channel")

        self.__finish_interval_border_of_time_distance_plot = new_index

    @property
    def total_solar_frames(self) -> int:
        return self.__solar_frames_storage.get_number_of_frames_in_current_channel()

    @property
    def current_solar_frame(self) -> SolarFrame:
        i = self.__index_of_current_solar_frame
        return (self.__solar_frames_storage
                .get_solar_frame_by_index_from_current_channel(i))



@unique
class PreviewModeEnum(IntEnum):
    SOLAR_PREVIEW = 1
    DISTANCE_PLOT_PREVIEW = 2
    TEST_MODE_DISTANCE_PLOT_PREVIEW = 3


class SelectedPreviewMode:
    def __init__(self):
        self.__mode: PreviewModeEnum = PreviewModeEnum.SOLAR_PREVIEW

    def set_solar_preview_mode(self):
        self.__mode = PreviewModeEnum.SOLAR_PREVIEW

    def set_time_distance_mode(self):
        self.__mode = PreviewModeEnum.DISTANCE_PLOT_PREVIEW

    def set_distance_plot_debug_mode(self):
        self.__mode = PreviewModeEnum.TEST_MODE_DISTANCE_PLOT_PREVIEW

    @property
    def current_preview_mode(self) -> PreviewModeEnum:
        return self.__mode


class TimeDistancePlot:

    # TODO: Вынести дополнетельные параметры
    @classmethod
    def create_distance_plot_from_real_data(cls,
                                            bezier_mask: BezierMask,
                                            viewport_transform: ViewportTransform,
                                            cubedata: Cubedata):
        instance = TimeDistancePlot()
        number_of_slices_along_loop = 400
        width_of_one_step_on_result_time_distance_plot = 3
        length_time_distance_plot = cubedata.number_of_frames * width_of_one_step_on_result_time_distance_plot # 300
        height_time_distance_plot = number_of_slices_along_loop #560
        time_distance_plot_array = np.zeros((height_time_distance_plot, length_time_distance_plot))

        setattr(instance, "__viewport_transform", viewport_transform)
        setattr(instance, "__cubedata", cubedata)
        setattr(instance, "__width_one_step_time_distance_plot", width_of_one_step_on_result_time_distance_plot)
        setattr(instance, "__width_time_distance_plot", length_time_distance_plot)
        setattr(instance, "__height_time_distance_plot", height_time_distance_plot)

        coordinates = instance.__get_coordinates_of_pixels_from_bezier_mask(bezier_mask,
                                                                            number_of_slices_along_loop,
                                                                            True)

        for i in range(cubedata.number_of_frames):
            frame_content = cubedata.get_frame(i).frame_content

            line = instance.__get_time_distance_line(frame_content,
                                                     height_time_distance_plot,
                                                     width_of_one_step_on_result_time_distance_plot,
                                                     coordinates,
                                                     False)

            start_index = i * width_of_one_step_on_result_time_distance_plot
            finish_index = (i + 1) * width_of_one_step_on_result_time_distance_plot
            time_distance_plot_array.T[start_index:finish_index] = line.T

        # todo: надо ли ?
        time_distance_plot_array = gaussian_filter(time_distance_plot_array, sigma=3)
        setattr(instance, "__time_distance_plot_array", time_distance_plot_array)

        return instance

    @classmethod
    def create_debug_distance_plot(cls,
                                   bezier_mask: BezierMask,
                                   number_of_frames_need_to_use_for_create_time_distance_plot: int = 100):
        instance = TimeDistancePlot()
        cubedata: Cubedata = Cubedata.create_from_debug_data(number_of_frames_need_to_use_for_create_time_distance_plot)

        number_of_slices_along_loop = 400
        width_of_one_step_on_result_time_distance_plot = 3
        length_time_distance_plot = cubedata.number_of_frames * width_of_one_step_on_result_time_distance_plot # 300
        height_time_distance_plot = number_of_slices_along_loop #560
        time_distance_plot_array = np.zeros((height_time_distance_plot, length_time_distance_plot))

        coordinates = instance.__get_coordinates_of_pixels_from_bezier_mask(bezier_mask,
                                                                            number_of_slices_along_loop,
                                                                            False)

        for i in range(cubedata.number_of_frames):
            frame_content = cubedata.get_frame(i).frame_content


            line = instance.__get_time_distance_line(frame_content,
                                                     height_time_distance_plot,
                                                     width_of_one_step_on_result_time_distance_plot,
                                                     coordinates,
                                                     True)

            start_index = i * width_of_one_step_on_result_time_distance_plot
            finish_index = (i + 1) * width_of_one_step_on_result_time_distance_plot
            time_distance_plot_array.T[start_index:finish_index] = line.T

        time_distance_plot_array = gaussian_filter(time_distance_plot_array, sigma=3)

        setattr(instance, "__cubedata", cubedata)
        setattr(instance, "__width_one_step_time_distance_plot", width_of_one_step_on_result_time_distance_plot)
        setattr(instance, "__width_time_distance_plot", length_time_distance_plot)
        setattr(instance, "__height_time_distance_plot", height_time_distance_plot)
        setattr(instance, "__time_distance_plot_array", time_distance_plot_array)
        return instance

    def __get_time_distance_line(self,
                                 frame: npt.NDArray,
                                 height_time_distance_plot,
                                 width_of_one_step_on_result_time_distance_plot,
                                 pixels_coordinates: List[List[QPoint]],
                                 is_debug: bool) -> npt.NDArray:
        number_of_slices = len(pixels_coordinates)
        time_distance_line = np.zeros((number_of_slices, width_of_one_step_on_result_time_distance_plot))

        for i, coordinates_of_pixels_of_one_slice in enumerate(pixels_coordinates):
            value: int = self.__get_mean_value_of_cross_slice(frame, coordinates_of_pixels_of_one_slice, is_debug)
            time_distance_line[i] = value

        return time_distance_line

    def __get_mean_value_of_cross_slice(self,
                                        frame: npt.NDArray,
                                        coordinates_of_pixels_of_one_slice: List[QPoint],
                                        is_debug: bool) -> int:
        accumulator = 0

        for coordinate_of_pixel in coordinates_of_pixels_of_one_slice:
            pixel_x_coordinate = coordinate_of_pixel.x()
            pixel_y_coordinate = coordinate_of_pixel.y()
            pixel_value = 0
            if is_debug:
                pixel_value = frame[pixel_y_coordinate][pixel_x_coordinate]
            else:
                pixel_value = frame[4095 - pixel_y_coordinate][pixel_x_coordinate]
            accumulator += pixel_value

        return int(accumulator / len(coordinates_of_pixels_of_one_slice))

    def get_time_distance_plot_as_qpixmap_in_grayscale(self) -> QPixmap:
        frame = getattr(self, "__time_distance_plot_array")
        width = getattr(self, "__width_time_distance_plot")
        height = getattr(self, "__height_time_distance_plot")

        data = frame.astype(np.uint8)
        qimage = QImage(data, width, height, QImage.Format_Grayscale8)
        return QPixmap.fromImage(qimage)

    def get_time_distance_plot_as_qpixmap_using_cmap_of_channel(self, channel: int):
        cm = get_cmap_by_channel(channel)

        frame = getattr(self, "__time_distance_plot_array")

        sp = SubplotParams(left=0., bottom=0., right=1., top=1.)
        l = frame.shape[1] / 100
        h = frame.shape[0] / 100
        fig = Figure(figsize=(l, h), dpi=100, subplotpars=sp)
        canvas = FigureCanvas(fig)
        axes = fig.add_subplot()
        axes.set_axis_off()
        axes.imshow(frame, cmap=cm)
        axes.imshow(frame.astype(np.float32), cmap=cm)
        canvas.draw()
        width, height = int(fig.figbbox.width), int(fig.figbbox.height)
        im = QImage(canvas.buffer_rgba(), width, height, QImage.Format_RGBA8888)
        return QPixmap.fromImage(im)

    def get_border_of_time_distance_slice(self, t: float) -> [int, int]:
        width_one_step = getattr(self, "__width_one_step_time_distance_plot")
        cubedata: Cubedata = getattr(self, "__cubedata")
        i = int(t * cubedata.number_of_frames)
        start_index = i * width_one_step
        finish_index = (i + 1) * width_one_step
        return start_index, finish_index

    def __get_coordinates_of_pixels_from_bezier_mask(self,
                                                     bezier_mask: BezierMask,
                                                     number_of_slices_along_loop: int,
                                                     need_to_tronsform_for_viewport_to_image: bool) -> List[List[QPoint]]:
        coordinates: List[List[QPoint]] = list()
        bottom_points: List[QPoint] = bezier_mask.get_bottom_border(number_of_slices_along_loop)
        top_points: List[QPoint] = bezier_mask.get_top_border(number_of_slices_along_loop)
        for i in range(number_of_slices_along_loop):
            bottom_point: QPoint = bottom_points[i]
            top_point: QPoint = top_points[i]

            if need_to_tronsform_for_viewport_to_image:
                viewport_transform: ViewportTransform = getattr(self, "__viewport_transform")
                bottom_point = viewport_transform.transform_from_viewport_pixel_to_image_pixel(bottom_point)
                top_point = viewport_transform.transform_from_viewport_pixel_to_image_pixel(top_point)

            pixels_coordinates = get_pixels_of_line(bottom_point.x(),
                                                    bottom_point.y(),
                                                    top_point.x(),
                                                    top_point.y())
            coordinates.append(pixels_coordinates)
        return coordinates

    def save_as_png(self, path_to_save: str, current_channel: int):
        cm = get_cmap_by_channel(current_channel)
        frame = getattr(self, "__time_distance_plot_array")
        sp = SubplotParams(left=0., bottom=0., right=1., top=1.)
        l = frame.shape[1] / 100
        h = frame.shape[0] / 100
        fig = Figure(figsize=(l, h), dpi=100, subplotpars=sp)
        canvas = FigureCanvas(fig)
        axes = fig.add_subplot()
        axes.set_axis_off()
        axes.imshow(frame, cmap=cm)
        axes.imshow(frame.astype(np.float32), cmap=cm)
        canvas.draw()
        fig.savefig(path_to_save)

    def save_numpy_array(self, path_to_save: str):
        frame: npt.NDArray = getattr(self, "__time_distance_plot_array")
        np.save(path_to_save, frame)

class AppModel:
    def __init__(self, configuration_app: 'ConfigurationApp'):
        self.__path_to_export_result = configuration_app.path_to_export_results #path_to_export_result
        self.__viewport_transform = ViewportTransform()
        self.__solar_frames_storage = SolarFramesStorage(self.__viewport_transform, configuration_app)
        self.__time_line = TimeLine(self.__solar_frames_storage)
        self.__current_channel = CurrentChannel(self.__solar_frames_storage, configuration_app.initial_channel)
        self.__bezier_mask = BezierMask()
        self.__interesting_solar_region = InterestingSolarRegion()
        self.__test_animated_frame = TestAnimatedFrame("horizontal", 30, 600)
        self.__selected_preview_mode = SelectedPreviewMode()

        self.__observers = []

    @property
    def path_to_export_result(self) -> str:
        return self.__path_to_export_result

    @property
    def solar_frames_storage(self) -> SolarFramesStorage:
        return self.__solar_frames_storage

    @property
    def viewport_transform(self) -> ViewportTransform:
        return self.__viewport_transform

    @property
    def time_line(self) -> TimeLine:
        return self.__time_line

    @property
    def current_channel(self) -> CurrentChannel:
        return self.__current_channel

    @property
    def bezier_mask(self) -> BezierMask:
        return self.__bezier_mask

    @property
    def interesting_solar_region(self) -> InterestingSolarRegion:
        return self.__interesting_solar_region

    @property
    def configuration(self) -> ConfigurationApp:
        return self.__configuration

    @property
    def test_animated_frame(self) -> TestAnimatedFrame:
        return self.__test_animated_frame

    @property
    def selected_preview_mode(self) -> SelectedPreviewMode:
        return self.__selected_preview_mode

    def add_observer(self, in_observer):
        self.__observers.append(in_observer)

    def remove_observer(self, in_observer):
        self.__observers.remove(in_observer)

    def notify_observers(self):
        if self.__current_channel.current_channel_was_changed:
            channel_need_to_load = self.__current_channel.channel
            self.__solar_frames_storage.cache_channel(channel_need_to_load)
        for x in self.__observers:
            x.model_is_changed()


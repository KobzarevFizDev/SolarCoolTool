import math
import os
import glob
import sqlite3
from typing import List, Tuple, Optional
from enum import IntEnum, unique
import time


from TimeDistancePlotBuilder.dda import get_pixels_of_line, get_pixels_of_cicle
from scipy.ndimage import zoom, gaussian_filter
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure, SubplotParams
from matplotlib import pyplot as plt
from matplotlib.colors import Colormap

import numpy as np
from PyQt5.QtCore import QPoint, QPointF, QRect, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtCore import QCoreApplication, QRect
import sunpy.map
import sunpy.data.sample
import sunpy.visualization.colormaps.cm
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from astropy.io import fits
import numpy.typing as npt

from TimeDistancePlotBuilder import transformations

from TimeDistancePlotBuilder.configuration import ConfigurationApp

from TimeDistancePlotBuilder.Exceptions.exceptions import IncorrectZoneInterestingSize, NotFoundDataForExport, DataForExportNotValid


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
    def content(self) -> npt.NDArray:
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
    
    @property
    def time_step_in_seconds(self) -> int:
        return 12

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
        frame_content = self.get_frame_by_t(t).content
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
        m.data[np.isnan(m.data)] = 0
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


class SolarFramesStorage(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int, int, str)
    error = pyqtSignal(str)

    def __init__(self, viewport_transform: 'ViewportTransform', configuration_app: 'ConfigurationApp'):
        super().__init__()
        self.__viewport_transform = viewport_transform
        self.__configuration_app = configuration_app
        self.__current_channel: int = configuration_app.initial_channel
        self.__path_to_directory: str = configuration_app.path_to_solar_images
        self.__loaded_channel: List[SolarFrame] = list()
        self.__initialize_database()

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

    @pyqtSlot()
    def load_channel(self, channel: int):
        step = self.__configuration_app.get_step_for_channel(channel)
        limit = self.__configuration_app.get_limit_for_channel(channel)
        need_to_skip = step - 1
        number_of_cached_frames = 0

        self.__current_channel = channel
        self.__loaded_channel.clear()

        files = self.__get_files_in_channel(channel)
        ids = self.__get_ids_of_frames_in_channel(channel)
        dates = self.__get_dates_of_files_in_channel(channel)

        for i, path in enumerate(files):
            if number_of_cached_frames > limit:
                print("Acheve limit")
                break
            print(f"caching {number_of_cached_frames}/{len(files)}. i = {i}")

            if need_to_skip > 0:
                print(f"skip {i}")
                need_to_skip -= 1
                continue

            number_of_cached_frames += 1
            id = ids[i]
            date = dates[i]
            solar_frame = SolarFrame(id, path, channel, date)
            solar_frame.set_viewport_transform(self.__viewport_transform)

            self.__loaded_channel.append(solar_frame)

            need_to_skip = step - 1

            self.progress.emit(number_of_cached_frames, limit, path)
            QCoreApplication.processEvents()

        self.finished.emit()

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

    def point_at_t(self, t: float) -> QPoint:
        A = (1-t)**3 * self.__p0
        B = 3 * (1-t)**2 * t * self.__p1
        C = 3 * (1-t)*t**2 * self.__p2
        D = t**3 * self.__p3

        return A + B + C + D

    # todo: удалить, оставить только функции которые возвращают нормализованные значения
    def tangent_at_t(self, t: float) -> QPoint:
        A = 3 * (1-t)**2 * (self.__p1 - self.__p0)
        B = 6 * (1 - t) * t * (self.__p2 - self.__p1)
        C = 3 * t**2 * (self.__p3 - self.__p2)
        return A + B + C
    
    def get_normalized_tangent_at_t(self, t: float) -> QPoint:
        tangent: QPoint = self.tangent_at_t(t)
        norm: float = math.sqrt(tangent.x() ** 2 + tangent.y() ** 2)
        return QPoint(tangent.x() / norm, tangent.y() / norm)

    def normal_at_t(self, t: float) -> QPoint:
        tangent = self.tangent_at_t(t)
        return QPoint(tangent.y(), -tangent.x())
    
    def get_normalized_normal_at_t(self, t: float) -> QPointF:
        normal: QPoint = self.normal_at_t(t)
        norm = math.sqrt(normal.x() ** 2 + normal.y() ** 2)
        return QPointF(normal.x() / norm, normal.y() / norm)
    
    def arc_length(self, t: float) -> float:
        integrand = lambda t: (tangent := self.tangent_at_t(t)) and np.linalg.norm([tangent.x(), tangent.y()])
        length, _ = quad(integrand, 0, t)
        return length 
    
    def find_t_for_equal_distances(self, number_of_points: int) -> List[float]:
        total_length: float = self.arc_length(1)
        segment_length: float = total_length / (number_of_points - 1)
        t_values = [0]

        for i in range(1, number_of_points - 1):
            target_length: float = i * segment_length
            func = lambda t: abs(self.arc_length(t) - target_length)
            print('start')
            result = minimize_scalar(func, bounds=(0, 1), method="bounded", tol=1e-2)
            print('finish')
            t_values.append(result.x)

        t_values.append(1)
        return t_values

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
    
    @property
    def length_in_pixels(self) -> float:
        return self.__bezier_curve.arc_length(1)

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
    
    def get_slices(self, number_of_slices: int, is_uniformly: bool) -> List[Tuple[QPoint, QPoint]]:
        t_values: List[float] = self.__get_t_values_for_slices(number_of_slices, is_uniformly)
        slices = list()
        for t in t_values:
            bottom_point: QPointF = QPointF(self.__bezier_curve.point_at_t(t))
            normal: QPoint = self.__bezier_curve.get_normalized_normal_at_t(t)
            offset: QPoint = QPoint( int(normal.x() * (self.__width_in_pixels)), int(normal.y() * (self.__width_in_pixels)) )
            top_point: QPoint = bottom_point + offset
            slices.append([bottom_point, top_point])
        return slices
    
    def __get_t_values_for_slices(self, number_of_slices: int , is_uniformly: bool) -> List[float]:
        if is_uniformly:
            return self.__bezier_curve.find_t_for_equal_distances(number_of_slices)
        else:
            return [(0.5 + i) * (1 / number_of_slices) for i in range(number_of_slices)]

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


class ZoneInteresting:
    def __init__(self):
        self.__size: int = 300 
        self.__position: QPoint = QPoint(300, 300)
        self.__previous_position_of_size_anchor: QPoint = QPoint(-1, -1)
        self.__delta_move_of_size_anchor: float = 0

    def set_position_of_position_anchor(self, anchor_pos: QPoint) -> None:
        anchor_pos_x: int = anchor_pos.x()
        anchor_pos_y: int = anchor_pos.y()
        pos_x: int = anchor_pos_x - self.__size // 2
        pos_y: int = anchor_pos_y + self.__size // 2
        self.__position = QPoint(pos_x, pos_y)
        self.__previous_position_of_size_anchor = self.top_left_in_view


    def set_position_of_size_anchor(self, anchor_pos: QPoint) -> None:
        if self.__previous_position_of_size_anchor == QPoint(-1, -1):
            self.__previous_position_of_size_anchor = anchor_pos
            return
 
        dir_to_zoom_x, dir_to_zoom_y = self.__get_direction_to_zoom()
        len_of_zoom_direction = self.__get_len_of_direction(dir_to_zoom_x, dir_to_zoom_y)
        anchor_direction_x, anchor_direction_y = self.__get_size_anchor_move_delta(anchor_pos)
        normalized_dir_to_zoom_x, normalized_dir_to_zoom_y = self.__get_normalized_direction(dir_to_zoom_x, dir_to_zoom_y)
        projection = (anchor_direction_x * normalized_dir_to_zoom_x + anchor_direction_y * normalized_dir_to_zoom_y) / len_of_zoom_direction

        diagonal_delta = projection * len_of_zoom_direction / math.sqrt(2)
        self.__delta_move_of_size_anchor += diagonal_delta * 2

        integer_part_of_delta_move, fractional_part_of_delta_move = divmod(self.__delta_move_of_size_anchor, 1)
        self.__delta_move_of_size_anchor -= integer_part_of_delta_move

        self.__size -= int(integer_part_of_delta_move)

        self.__previous_position_of_size_anchor = anchor_pos


    def __get_direction_to_zoom(self): 
        direction_to_zoom_x: int = self.bottom_right_in_view.x() - self.top_left_in_view.x()
        direction_to_zoom_y: int = self.bottom_right_in_view.y() - self.top_left_in_view.y()
        return direction_to_zoom_x, direction_to_zoom_y
    
    def __get_size_anchor_move_delta(self, anchor_pos: QPoint):
        previous_x: int = self.__previous_position_of_size_anchor.x()
        previous_y: int = self.__previous_position_of_size_anchor.y()

        new_x: int = anchor_pos.x()
        new_y: int = anchor_pos.y()

        anchor_direction_x = new_x - previous_x
        anchor_direction_y = new_y - previous_y

        return anchor_direction_x, anchor_direction_y
    
    def __get_len_of_direction(self, dir_x, dir_y) -> float:
        return math.sqrt(dir_x**2 + dir_y**2)
    
    
    def __get_normalized_direction(self, dir_x, dir_y):
        len_of_dir: float = math.sqrt(dir_x**2 + dir_y**2)
        return (dir_x / len_of_dir), (dir_y / len_of_dir)
    
    @property
    def size(self) -> QPoint:
        return self.__size

    @property
    def position(self) -> QPoint:
        return self.__position

    @property
    def top_right_in_view(self) -> QPoint:
        pos_x: int = self.__position.x()
        pos_y: int = self.__position.y()
        half_size: int = int(self.__size / 2)
        return QPoint(int(pos_x + half_size), int(pos_y + half_size))

    @property
    def top_left_in_view(self) -> QPoint:
        pos_x: int = self.__position.x()
        pos_y: int = self.__position.y()
        half_size: int = int(self.__size / 2)
        return QPoint(int(pos_x - half_size), int(pos_y + half_size))
        
    @property
    def bottom_left_in_view(self) -> QPoint:
        pos_x: int = self.__position.x()
        pos_y: int = self.__position.y()
        half_size: int = int(self.__size / 2)
        return QPoint(int(pos_x - half_size), int(pos_y - half_size))

    @property
    def bottom_right_in_view(self) -> QPoint:
        pos_x: int = self.__position.x()
        pos_y: int = self.__position.y()
        half_size: int = int(self.__size / 2)
        return QPoint(int(pos_x + half_size), int(pos_y - half_size))
    
    def set_viewport_position(self, x: int, y: int) -> None:
        self.__position: QPoint = QPoint(x, y)
        pass

    def set_viewport_size(self, size: int) -> None:
        if size <= 0:
            raise IncorrectZoneInterestingSize(size)
        self.__size = size



# todo: Подумать над названием
class ViewportTransform:
    def __init__(self, zone_interesting: ZoneInteresting):
        self.__zone_interesting: ZoneInteresting = zone_interesting
        self.__zoom = 1
        self.__origin_size_image = 600
        self.__offset: QPoint = QPoint(0, 0)

    @property
    def dpi_of_bezier_mask_window(self) -> float:
        widget_size = 600
        dpi_of_solar_view: float = self.dpi_solar_view_window
        size_of_zone_interesting_in_image_pixels = dpi_of_solar_view * self.__zone_interesting.size
        dpi_of_bezier_mask_window = size_of_zone_interesting_in_image_pixels / widget_size
        return dpi_of_bezier_mask_window

    @property
    def dpi_solar_view_window(self) -> float:
        widget_size = 600
        image_size = 4096
        dpi_of_solar_view = image_size / (widget_size * self.__zoom)
        return dpi_of_solar_view
    
    @property
    def bezier_mask_px_size_in_megameters(self) -> float:
        size_of_px_in_megameters = 400
        return self.dpi_of_bezier_mask_window * size_of_px_in_megameters

    @property
    def solar_view_px_size_in_megameters(self) -> float:
        size_of_px_in_megameters = 400
        return self.dpi_solar_view_window * size_of_px_in_megameters

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


    def transform_point_from_bezier_mask_widget_to_fits(self, point_in_bezier_mask: QPoint) -> QPoint:
        size_of_fits = 4096
        position_of_zone_interesting: QPoint = self.__zone_interesting.position
        size_of_zone_interesting: int = self.__zone_interesting.size
        widget_size: int = 600

        point_in_solar_view =  transformations.transform_point_from_bezier_mask_to_solar_view(position_of_zone_interesting, 
                                                                                              point_in_bezier_mask,
                                                                                              size_of_zone_interesting,
                                                                                              widget_size)
        
        point_in_fits = transformations.transform_point_from_solar_view_to_fits(point_in_solar_view, 
                                                                                self.offset, 
                                                                                size_of_fits, 
                                                                                widget_size, 
                                                                                self.zoom)
        
        return point_in_fits

    # legacy -----------------------------------

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
    

    # legacy -----------------------------------

    def get_transformed_pixmap_for_viewport(self, solar_frame: SolarFrame) -> QPixmap:
        scale: int = int(self.__zoom * self.__origin_size_image)
        scaled_solar_frame = solar_frame.qtimage.scaled(scale, scale)
        pixmap_for_draw = QPixmap.fromImage(scaled_solar_frame)
        return pixmap_for_draw


class TimeLine:
    def __init__(self, solar_frames_storage: SolarFramesStorage):
        self.__solar_frames_storage: SolarFramesStorage = solar_frames_storage
        self.__index_of_current_solar_frame: int = 0
        self.__start_frame_to_build_tdp: int = 0
        self.__finish_frame_to_build_tdp: int = 0
        self.__current_tdp_step: int = 0

    @property
    def max_index_of_solar_frame_for_debug_tdp(self) -> int:
        return 400

    @property
    def max_index_of_solar_frame(self) -> int:
        return self.__solar_frames_storage.get_number_of_frames_in_current_channel()

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
    def start_frame_to_build_tdp(self) -> int:
        return self.__start_frame_to_build_tdp

    @start_frame_to_build_tdp.setter
    def start_frame_to_build_tdp(self, new_index) -> None:
        number_of_solar_frames_in_current_channel = self.__solar_frames_storage.get_number_of_frames_in_current_channel()
        if new_index >= number_of_solar_frames_in_current_channel:
            raise Exception(f"Index of start interval time distance plot cannot be >= number of solar frames in current channel. Index = {new_index}")

        self.__start_frame_to_build_tdp = new_index

    @property
    def finish_frame_to_build_tdp(self) -> int:
        return self.__finish_frame_to_build_tdp

    @finish_frame_to_build_tdp.setter
    def finish_frame_to_build_tdp(self, new_index) -> None:
        number_of_solar_frames_in_current_channel = self.__solar_frames_storage.get_number_of_frames_in_current_channel()
        if new_index >= number_of_solar_frames_in_current_channel:
            raise Exception("Index of finish interval time distance plot cannot be >= number of solar frames in current channel")

        self.__finish_frame_to_build_tdp = new_index

    @property
    def total_solar_frames(self) -> int:
        return self.__solar_frames_storage.get_number_of_frames_in_current_channel()

    @property
    def current_solar_frame(self) -> SolarFrame:
        i = self.__index_of_current_solar_frame
        return (self.__solar_frames_storage
                .get_solar_frame_by_index_from_current_channel(i))
    
    @property
    def solar_frame_by_current_tdp_step(self) -> SolarFrame:
        i = self.__current_tdp_step
        return (self.__solar_frames_storage
                .get_solar_frame_by_index_from_current_channel(i))

    @property
    def tdp_step(self) -> int:
        return self.__current_tdp_step

    @tdp_step.setter
    def tdp_step(self, value: int) -> None:
        self.__current_tdp_step = value

    def set_finish_index_of_build_tdp_as_maximum(self) -> None:
        self.finish_frame_to_build_tdp = self.max_index_of_solar_frame - 1


@unique
class AppStates(IntEnum):
    SOLAR_PREVIEW_STATE = 1
    BUILD_TDP_STATE = 2
    PREVIEW_PLOT_STATE = 3
    PUBLISH_TDP_STATE = 4

class CurrentAppState:
    def __init__(self):
        self.__state: AppStates = AppStates.SOLAR_PREVIEW_STATE

    def set_solar_preview_mode_state(self):
        self.__state = AppStates.SOLAR_PREVIEW_STATE

    def set_build_tdp_state(self):
        self.__state = AppStates.BUILD_TDP_STATE

    def set_preview_plot_state(self):
        self.__state = AppStates.PREVIEW_PLOT_STATE

    def set_publish_tdp_state(self):
        self.__state = AppStates.PUBLISH_TDP_STATE

    @property
    def current_state(self) -> AppStates:
        return self.__state

class TDP(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int, int)
    error = pyqtSignal(str)

    def __init__(self, bezier_mask: BezierMask, viewport_transform: ViewportTransform):
        super().__init__()
        self.__bezier_mask = bezier_mask
        self.__viewport_transform = viewport_transform

        self.__width_of_tdp_step = 3 # Толщина временного шага в пикселях (1 кадр это 3 пикселя в time distance plot)
        self.__ro = 0.5 # Плотность срезов (чем меньше тем реже срезы)
        self.__channel: int = -1
        
        self.__tdp_array: npt.NDArray = None
        self.__is_builded: bool = False

        self.__smooth_parametr: float = 0

        self.__is_new: bool = False
        self.__is_test: bool = False

    @property
    def is_new(self) -> bool:
        result = self.__is_new
        self.__is_new = False
        return result
    
    @property
    def is_test(self) -> bool:
        return self.__is_test

    # todo: проверика на то что channel корректный 
    @property
    def cmap(self) -> Colormap:
        if self.__channel != -1:
            return get_cmap_by_channel(self.__channel)
        else:
            return get_cmap_by_channel(131)

    @property
    def was_builded(self) -> bool:
        return self.__is_builded

    @property
    def width_of_tdp_step(self) -> int:
        return self.__width_of_tdp_step
    
    @property
    def total_tdp_steps(self) -> int:
        return self.__tdp_array.shape[1] // self.__width_of_tdp_step
    
    @property
    def length_of_tdp_in_px(self) -> int:
        return self.__tdp_array.shape[1]
    
    @property
    def time_step_in_seconds(self) -> int:
        if self.__is_builded == False:
            return 12 * self.__skip_frames
        else:
            return self.__time_step
        
    @property
    def tdp_array(self) -> npt.NDArray:
        return self.__tdp_array
    
    @property
    def smooth_parametr(self) -> float:
        return self.__smooth_parametr
    
    def set_smooth_parametr(self, value) -> None:
        if value < 0:
            raise Exception("Smooth parametr can not be negative")
        
        self.__smooth_parametr = value

    @pyqtSlot()
    def build(self, skip_frames: int, cubedata: Cubedata, channel: int, is_uniformly: bool) -> None:
        self.__time_step = cubedata.time_step_in_seconds
        self.__is_builded = True
        self.__is_test = False
        self.__channel = channel
        self.__skip_frames = skip_frames

        number_of_slices: int = self.__get_number_of_slices()
        slices: List[Tuple[QPoint, QPoint]] = self.__bezier_mask.get_slices(number_of_slices, is_uniformly)
        slices = self.__convert_slices_to_fits_coordinates(slices)

        self.__initialize_tdp_array(cubedata, number_of_slices)

        for index_of_step in range(cubedata.number_of_frames):
            frame: CubedataFrame = cubedata.get_frame(index_of_step)
            self.__handle_tdp_step(slices, frame, self.__width_of_tdp_step, index_of_step)

            self.progress.emit(index_of_step, cubedata.number_of_frames - 1)
            QCoreApplication.processEvents()


        self.__tdp_array = gaussian_filter(self.__tdp_array, sigma=self.__smooth_parametr)

        self.__is_new = True

        self.finished.emit()


    def build_test_tdp(self, number_of_frames: int) -> None:
        self.__time_step = 12
        self.__is_builded = True
        self.__is_test = True
        self.__channel = 131

        horizontal_length_of_tdp: int = number_of_frames * self.__width_of_tdp_step
        vertical_length_of_tdp: int = 500
        self.__tdp_array = np.zeros((vertical_length_of_tdp, horizontal_length_of_tdp))

        width_of_black_line = 200

        borders_indexes = [i * width_of_black_line for i in range(horizontal_length_of_tdp)]

        for i in range(len(borders_indexes) - 1):
            if i % 2 == 0:
                continue

            start_border: int = borders_indexes[i]
            finish_border: int = borders_indexes[i + 1]
            self.__tdp_array[:, start_border:finish_border] = 1

        self.__tdp_array = gaussian_filter(self.__tdp_array, sigma=self.__smooth_parametr)

        self.__is_new = True

    def get_placeholder(self, width_in_px: int, height_in_px: int) -> None:
        return np.zeros((height_in_px, width_in_px))

    def __get_number_of_slices(self) -> int:        
        dpi: float = self.__viewport_transform.dpi_of_bezier_mask_window 
        l: float = self.__bezier_mask.length_in_pixels
        number_of_slices = int(dpi * l * self.__ro) 
        return number_of_slices
    
    def __convert_slices_to_fits_coordinates(self, slices: List[Tuple[QPoint, QPoint]]) -> List[Tuple[QPoint, QPoint]]:
        for i in range(len(slices)):
            slice: Tuple[QPoint, QPoint] = slices[i]
            bp_in_bezier_mask_window_coordinates: QPoint = slice[0]
            tp_in_bezier_mask_window_coordinates: QPoint = slice[1]
            bp_in_fits_coordinates: QPoint = self.__viewport_transform.transform_point_from_bezier_mask_widget_to_fits(bp_in_bezier_mask_window_coordinates) 
            tp_in_fits_coordinates: QPoint = self.__viewport_transform.transform_point_from_bezier_mask_widget_to_fits(tp_in_bezier_mask_window_coordinates)
            slice[0] = bp_in_fits_coordinates
            slice[1] = tp_in_fits_coordinates
            slices[i] = slice
        return slices
    
    def __initialize_tdp_array(self, cubedata: Cubedata, number_of_slices: int) -> None:
        horizontal_length_of_tdp: int = cubedata.number_of_frames * self.__width_of_tdp_step
        vertical_length_of_tdp: int = number_of_slices
        self.__tdp_array = np.zeros((vertical_length_of_tdp, horizontal_length_of_tdp))
    
    def __handle_tdp_step(self, 
                          slices:List[Tuple[QPoint, QPoint]], 
                          frame: CubedataFrame,
                          width_of_step_in_pixels: int,
                          index_of_step: int) -> npt.NDArray:
        start_column_index = index_of_step * width_of_step_in_pixels
        finish_column_index = (index_of_step + 1) * width_of_step_in_pixels - 1
        columns_indexes = [i for i in range(start_column_index, finish_column_index + 1)]

        for i, slice in enumerate(slices):
            mean_value_of_slice: float = self.__get_mean_value_of_slice(slice, frame)
            self.__tdp_array[i,columns_indexes] = mean_value_of_slice

    def __get_mean_value_of_slice(self, slice: Tuple[QPoint, QPoint], frame: CubedataFrame) -> float:
        bp: QPoint = slice[0]
        tp: QPoint = slice[1]

        x1 = bp.x()
        y1 = bp.y()

        x2 = tp.x()
        y2 = tp.y()

        pixels_coordinates: List[QPoint] = get_pixels_of_line(x1, y1, x2, y2)

        count = 0
        total_sum = 0 

        for pixel_coordinate in pixels_coordinates:
            pixel_x: int = pixel_coordinate.x()
            pixel_y: int = pixel_coordinate.y()

            count += 1

            total_sum += frame.content[pixel_y][pixel_x] 

        mean_value = total_sum / count
        return mean_value

    def __vertical_resize_tdp_array(self, tdp_segment: npt.NDArray, new_vertical_size_in_px: float) -> npt.NDArray:
        old_vertical_size = tdp_segment.shape[0]
        vertical_zoom = new_vertical_size_in_px / old_vertical_size
        return zoom(tdp_segment, (vertical_zoom, 1), order=1)

    def get_full_pixmap(self) -> QPixmap:
        return self.convert_to_qpixmap(0, self.total_tdp_steps - 1, vertical_size_in_px=self.__tdp_array.shape[0])

    def convert_to_qpixmap(self, start_step: int, finish_step: int, vertical_size_in_px: int) -> QPixmap:
        cm = get_cmap_by_channel(self.__channel)
        sp = SubplotParams(left=0., bottom=0., right=1., top=1.)
        dpi_value = 100

        tdp: npt.NDArray = self.__tdp_array[ : , start_step * self.__width_of_tdp_step : (finish_step - 1) * self.__width_of_tdp_step]
        tdp = self.__vertical_resize_tdp_array(tdp, vertical_size_in_px)

        l = tdp.shape[1] / dpi_value
        h = tdp.shape[0] / dpi_value
        fig = Figure(figsize=(l, h), dpi=dpi_value, subplotpars=sp)
        canvas = FigureCanvas(fig)
        axes = fig.add_subplot()
        axes.set_axis_off()
        axes.imshow(tdp.astype(np.float32), cmap=cm)
        canvas.draw()
        width, height = int(fig.figbbox.width), int(fig.figbbox.height)
        im = QImage(canvas.buffer_rgba(), width, height, QImage.Format_RGBA8888)
        return QPixmap.fromImage(im)


# todo: Легаси
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
            frame_content = cubedata.get_frame(i).content

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
        length_time_distance_plot = cubedata.number_of_frames * width_of_one_step_on_result_time_distance_plot
        height_time_distance_plot = number_of_slices_along_loop
        time_distance_plot_array = np.zeros((height_time_distance_plot, length_time_distance_plot))

        coordinates = instance.__get_coordinates_of_pixels_from_bezier_mask(bezier_mask,
                                                                            number_of_slices_along_loop,
                                                                            False)

        for i in range(cubedata.number_of_frames):
            frame_content = cubedata.get_frame(i).content


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
            pixel_value = frame[pixel_y_coordinate][pixel_x_coordinate]
            accumulator += pixel_value

        return int(accumulator / len(coordinates_of_pixels_of_one_slice))
    
    def __get_coordinates_of_pixels_from_bezier_mask(self,
                                                     bezier_mask: BezierMask,
                                                     number_of_slices_along_loop: int,
                                                     need_to_transform_for_viewport_to_image: bool) -> List[List[QPoint]]:
        coordinates: List[List[QPoint]] = list()
        bottom_points: List[QPoint] = bezier_mask.get_bottom_border(number_of_slices_along_loop)
        top_points: List[QPoint] = bezier_mask.get_top_border(number_of_slices_along_loop)
        for i in range(number_of_slices_along_loop):
            bottom_point: QPoint = bottom_points[i]
            top_point: QPoint = top_points[i]

            if need_to_transform_for_viewport_to_image:
                viewport_transform: ViewportTransform = getattr(self, "__viewport_transform")
                bottom_point = viewport_transform.transform_point_from_bezier_mask_widget_to_fits(bottom_point)
                top_point = viewport_transform.transform_point_from_bezier_mask_widget_to_fits(top_point)

            pixels_coordinates = get_pixels_of_line(bottom_point.x(),
                                                    bottom_point.y(),
                                                    top_point.x(),
                                                    top_point.y())
            coordinates.append(pixels_coordinates)
        return coordinates

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


class SelectedBezierSegments:
    def __init__(self, number_of_bizer_segments: int):
        self.__number_of_segments: int = number_of_bizer_segments
        self.__statuses: List[bool] = [False for _ in range(number_of_bizer_segments)]

    def set_segment_as_selected(self, index: int) -> None:
        self.__statuses[index] = True

    def set_segment_as_unselected(self, index: int) -> None:
        self.__statuses[index] = False

    def status_of_segment(self, index: int) -> bool:
        return self.__statuses[index]
    
    @property
    def number_of_bizer_segments(self) -> int:
        return self.__number_of_segments

class Export:
    def __init__(self, directory_with_export: str):
        self.__directory_with_export: str = directory_with_export

    def __find_file_with_extenstion(self, extension: str) -> List[str]:
        return glob.glob(os.path.join(self.__directory_with_export, extension))

    @property
    def path_to_png_file(self) -> str:
        png_files = self.__find_file_with_extenstion('.png')
        if len(png_files) == 1:
            raise DataForExportNotValid()

    @property
    def path_to_numpy_file(self) -> str:
        numpy_files = self.__find_file_with_extenstion('.npy')
        if len(numpy_files) == 1:
            raise DataForExportNotValid()
    
    @property
    def path_to_animation_loop_file(self) -> str:
        animation_files = self.__find_file_with_extenstion('.mp4')
        if len(animation_files) == 1:
            raise DataForExportNotValid()

class LastExport:
    def __init__(self, path_to_export_result: str):
        self.__path_to_export_result = path_to_export_result

    def __get_directory_with_latest_export(self) -> Optional[str]:
        directories = [d for d in glob.glob(os.path.join(self.__path_to_export_result, '*')) if os.path.isdir(d)]
        directories.sort(key=os.path.getctime, reverse=True)
        if directories:
            directories[0]
        else:
            None

    @property
    def last_export(self) -> Export:
        directory_with_last_save: str = self.__get_directory_with_latest_export()
        if directory_with_last_save == None:
            raise NotFoundDataForExport()
        else:
            return Export(directory_with_last_save)
    

class LoopAnimation:
    def __init__(self, 
                 bezier_mask: BezierMask, 
                 time_line: TimeLine, 
                 solar_frame_storage: SolarFramesStorage,
                 zone_interesting: ZoneInteresting):
        self.__bezier_mask = bezier_mask
        self.__time_line = time_line
        self.__solar_frame_storage = solar_frame_storage
        self.__zone_interesting = zone_interesting

    def get_frames_for_animation(self) -> List[npt.NDArray]:
        frames = list()
        pixmapes: List[QPixmap] = self.__get_pixmapes_for_animation()
        for pixmap in pixmapes:
            image = pixmap.toImage()
            width, height = image.width(), image.height()
            width, height = image.width(), image.height()
            buffer = image.bits().asstring(image.byteCount())  
            arr = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 4)) 
            frames.append(arr[:, :, [2,1,0]])
        return frames 

    def __get_pixmapes_for_animation(self) -> List[QPixmap]:
        pixmapes = list()
        top_right: QPoint = self.__zone_interesting.top_right_in_view
        bottom_left: QPoint = self.__zone_interesting.bottom_left_in_view
        for i in range(self.__time_line.start_frame_to_build_tdp, self.__time_line.finish_frame_to_build_tdp):
            solar_frame: SolarFrame = self.__solar_frame_storage.get_solar_frame_by_index_from_current_channel(i)
            pixmap: QPixmap = solar_frame.get_pixmap_of_solar_region(bottom_left, top_right)
            pixmapes.append(pixmap)

        pixmapes = self.__draw_loop_selection(pixmapes)

        pixmapes = self.__get_croped_frames(pixmapes)

        return pixmapes

    
    def __draw_loop_selection(self, frames: List[QPixmap]) -> List[QPixmap]:
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(4)
        for frame in frames:
            painter = QPainter(frame)
            painter.setPen(pen)
            
            bottom_border_points: List[QPoint] = self.__bezier_mask.get_bottom_border()
            top_border_points: List[QPoint] = self.__bezier_mask.get_top_border()

            previous: Optional[QPoint] = None

            for current in bottom_border_points:
                if previous != None:
                    painter.drawLine(previous.x(), previous.y(), current.x(), current.y())
                
                previous = current

            previous = None
            for current in top_border_points:
                if previous != None:
                    painter.drawLine(previous.x(), previous.y(), current.x(), current.y())
                
                previous = current

            painter.drawLine(bottom_border_points[0].x(), bottom_border_points[0].y(), top_border_points[0].x(), top_border_points[0].y())
            painter.drawLine(bottom_border_points[-1].x(), bottom_border_points[-1].y(), top_border_points[-1].x(), top_border_points[-1].y())
            painter.end()

        return frames

    def __get_croped_frames(self, frames: List[QPixmap]) -> List[QPixmap]:
        croped_frames = []

        rect = self.__get_bounding_points()

        for frame in frames: 
            croped_frame: QPixmap = frame.copy(rect)
            croped_frames.append(croped_frame)
        return croped_frames

    def __get_bounding_points(self) -> QRect:
        offset = self.__bezier_mask.width_in_pixels

        top_border_points: List[QPoint] = self.__bezier_mask.get_top_border()
        max_y: int = max([p.y() for p in top_border_points])
        max_x: int = max([p.x() for p in top_border_points])

        min_y: int = min([p.y() for p in top_border_points])
        min_x: int = min([p.x() for p in top_border_points])

        bl = QPoint(min_x, max_y)
        tl = QPoint(min_x, min_y)

        br = QPoint(max_x, max_y)
        tr = QPoint(max_x, min_y)

        center_x = QPoint((bl + br)).x() // 2
        center_y = QPoint((tl + bl)).y() // 2
 
        width: int = br.x() - bl.x()
        height: int = br.y() - tr.y()
        max_side = max(width, height)

        center = QPoint(center_x, center_y)

        bl = QPoint(center.x() - max_side // 2 - offset, center.y() - max_side // 2 - offset)
        br = QPoint(center.x() + max_side // 2 + offset, center.y() - max_side // 2 - offset)

        tl = QPoint(center.x() - max_side // 2 - offset, center.y() + max_side // 2 + offset)
        tr = QPoint(center.x() + max_side // 2 + offset, center.y() + max_side // 2 + offset)

        rect = QRect(bl.x(), bl.y(), max_side + 2 * offset, max_side + 2 * offset)

        return rect 

class AppModel:
    def __init__(self, configuration_app: 'ConfigurationApp'):
        self.__configuration = configuration_app
        self.__path_to_export_result = configuration_app.path_to_export_results
        self.__zone_interesting = ZoneInteresting()
        self.__viewport_transform = ViewportTransform(self.__zone_interesting)
        self.__solar_frames_storage = SolarFramesStorage(self.__viewport_transform, configuration_app)
        self.__time_line = TimeLine(self.__solar_frames_storage)
        self.__current_channel = CurrentChannel(self.__solar_frames_storage, configuration_app.initial_channel)
        self.__bezier_mask = BezierMask()
        self.__test_animated_frame = TestAnimatedFrame("horizontal", 30, 600)
        self.__app_state = CurrentAppState()
        self.__selected_bezier_segments = SelectedBezierSegments(10)
        self.__tdp = TDP(self.__bezier_mask, self.__viewport_transform)

        self.__loop_animation = LoopAnimation(self.__bezier_mask, self.__time_line, self.__solar_frames_storage, self.__zone_interesting)

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
    def zone_interesting(self) -> ZoneInteresting:
        return self.__zone_interesting

    @property
    def configuration(self) -> ConfigurationApp:
        return self.__configuration

    @property
    def test_animated_frame(self) -> TestAnimatedFrame:
        return self.__test_animated_frame

    @property
    def app_state(self) -> CurrentAppState:
        return self.__app_state
    
    @property
    def selected_bezier_segments(self) -> SelectedBezierSegments:
        return self.__selected_bezier_segments
    
    @property
    def time_distance_plot(self) -> TDP:
        return self.__tdp
    
    @property
    def loop_animation(self) -> LoopAnimation:
        return self.__loop_animation

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


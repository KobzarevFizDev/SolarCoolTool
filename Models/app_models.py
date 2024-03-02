import math
import os
import sqlite3
from typing import List

import numpy as np
from PyQt5.QtCore import QPoint
import transformations
import sunpy.visualization.colormaps.cm
from PyQt5.QtGui import QImage
from astropy.io import fits
import numpy.typing as npt


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
    def number_of_segments(self) -> int:
        return self.__number_of_segments

    def __create_initial_bezier_curve(self) -> BezierCurve:
        bezier_curve = BezierCurve(QPoint(100, 100),
                                   QPoint(200, 200),
                                   QPoint(300, 150),
                                   QPoint(400, 300))
        return bezier_curve

    def __get_longitudinal_slice(self):
        pass

    def get_top_border(self) -> List[QPoint]:
        border_points: List[QPoint] = list()
        for i in range(self.__number_of_segments + 1):
            t = i / self.__number_of_segments
            normal_at_t: QPoint = self.__bezier_curve.normal_at_t(t)
            magnitude_of_normal = math.sqrt(normal_at_t.x() ** 2 + normal_at_t.y() ** 2)
            border_point = normal_at_t + QPoint(self.__width_in_pixels * normal_at_t.x() / magnitude_of_normal,
                                                self.__width_in_pixels * normal_at_t.y() / magnitude_of_normal)
            border_points.append(border_point)
        return border_points

    def get_bottom_border(self) -> List[QPoint]:
        border_points: List[QPoint] = list()
        for i in range(self.__number_of_segments + 1):
            t = i / self.__number_of_segments
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


class CurrentChannel:
    def __init__(self, initial_channel=94):
        self.__available_channels = [94, 131, 171, 193, 211, 355]
        self.__current_channel: int = initial_channel \
            if self.__is_this_channel_available(initial_channel) \
            else self.__available_channels[0]
        self.__current_channel_was_changed: bool = False

    @property
    def channel(self) -> int:
        return self.__current_channel

    @channel.setter
    def channel(self, new_channel) -> None:
        if self.__is_this_channel_available(new_channel):
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
        return 100

    def __is_this_channel_available(self, channel: int) -> bool:
        return channel in self.__available_channels


class InterestingSolarRegion:
    def __init__(self):
        self.__top_right: QPoint = QPoint(600, 0)
        self.__bottom_left: QPoint = QPoint(0, 600)

        self.__top_right_point_was_selected: bool = False
        self.__bottom_left_point_was_selected: bool = False

    @property
    def top_right(self) -> QPoint:
        if self.__top_right_point_was_selected:
            self.__top_right_point_was_selected = False
            return self.__top_right
        else:
            raise Exception("Top right point was not selected")

    @property
    def bottom_left(self) -> QPoint:
        if self.__bottom_left_point_was_selected:
            self.__bottom_left_point_was_selected = False
            return self.__bottom_left
        else:
            raise Exception("Bottom left point was not selected")

    def set_top_right(self, point: QPoint) -> None:
        self.__top_right_point_was_selected = True
        self.__top_right = point
        if self.__top_right_point_was_selected and self.__bottom_left_point_was_selected:
            self.__align_to_square_if_necessary()

    def set_bottom_left(self, point: QPoint) -> None:
        self.__bottom_left_point_was_selected = True
        self.__bottom_left = point
        if self.__top_right_point_was_selected and self.__bottom_left_point_was_selected:
            self.__align_to_square_if_necessary()

    def __align_to_square_if_necessary(self) -> None:
        x_side_size = self.__top_right.x() - self.__bottom_left.x()
        y_side_size = self.__bottom_left.y() - self.__top_right.y()
        side_size = (x_side_size + y_side_size)/2
        half_side_size = side_size/2
        center_of_square = QPoint(int((self.__top_right.x() + self.__bottom_left.x())/2),
                                  int((self.__top_right.x() + self.__bottom_left.y())/2))

        self.__top_right = QPoint(int(center_of_square.x() + half_side_size),
                                  int(center_of_square.y() + half_side_size))
        self.__bottom_left = QPoint(int(center_of_square.x() - half_side_size),
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

class TimeLine:
    def __init__(self):
        self.__number_of_solar_frames_in_current_channel: int = 0
        self.__index_of_current_solar_frame: int = 0

    @property
    def number_of_solar_frames_in_current_channel(self) -> int:
        return self.__number_of_solar_frames_in_current_channel

    @number_of_solar_frames_in_current_channel.setter
    def number_of_solar_frames_in_current_channel(self, value) -> None:
        if value < 0:
            raise Exception("Number of solar frames cannot be negative")
        self.__number_of_solar_frames_in_current_channel = value

    @property
    def index_of_current_solar_frame(self) -> int:
        return self.__index_of_current_solar_frame

    @index_of_current_solar_frame.setter
    def index_of_current_solar_frame(self, index) -> None:
        if index >= self.__number_of_solar_frames_in_current_channel:
            raise Exception("Index of current solar frame cannot be >= number of solar frames in current channel")
        self.__index_of_current_solar_frame = index


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
        self.__pixels_array: npt.NDArray = self.__get_pixels_array()
        self.__qimage = self.__get_qtimage()


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

    def __get_pixels_array(self) -> npt.NDArray:
        hdul = fits.open(self.__path_to_fits_file)
        pixels_array = hdul[1].data
        hdul.close()
        return pixels_array

    def __get_qtimage(self) -> QImage:
        img_w = self.__pixels_array.shape[0]
        img_h = self.__pixels_array.shape[1]
        cm = {94: sunpy.visualization.colormaps.cm.sdoaia94,
              131: sunpy.visualization.colormaps.cm.sdoaia131,
              171: sunpy.visualization.colormaps.cm.sdoaia171,
              193: sunpy.visualization.colormaps.cm.sdoaia193,
              211: sunpy.visualization.colormaps.cm.sdoaia211,
              304: sunpy.visualization.colormaps.cm.sdoaia304,
              355: sunpy.visualization.colormaps.cm.sdoaia335}[self.__channel]

        a = np.array(255 * cm(self.__pixels_array), dtype=np.uint8)
        qimage = QImage(a, img_h, img_w, 4 * img_w, QImage.Format_RGBA8888)
        return qimage

# todo: Валидацию на корректное значение channel
class SolarFramesStorage:
    def __init__(self,
                 initial_channel: int,
                 path_to_directory: str):
        self.__path_to_directory: str = path_to_directory
        self.__loaded_channel: List[SolarFrame] = list()
        self.__initialize_database()
        self.load_channel(initial_channel)

    def __initialize_database(self) -> None:
        files = self.__get_files_in_directory()
        channels = self.__get_channels(files)
        dates = self.__get_dates(files)

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
        relative_file_paths = list(filter((lambda f: "image" in f), os.listdir(self.__path_to_directory)))
        absolute_file_paths = [self.__path_to_directory + "\\" + rf for rf in relative_file_paths]
        return absolute_file_paths

    def __get_channels(self, files) -> List[int]:
        return [f.split('.')[3] for f in files]

    def __get_dates(self, files) -> List[str]:
        return [f.split('.')[2][0:10] for f in files]

    def load_channel(self, channel: int) -> None:
        self.__loaded_channel.clear()

        files = self.__get_files_in_directory()
        ids = self.get_ids_of_frames_in_channel(channel)
        dates = self.__get_dates(files)

        for i, path in enumerate(files):
            id = ids[i]
            date = dates[i]
            solar_frame = SolarFrame(id, path, channel, date)
            self.__loaded_channel.append(solar_frame)

    def get_number_of_frames_in_channel(self, channel: int) -> int:
        connection = sqlite3.connect("my_database.db")
        cursor = connection.cursor()
        command = "SELECT Date FROM Images WHERE Channel = {0}".format(channel)
        number_of_images = int(cursor.execute(command).fetchall()[0][0])
        connection.close()
        return number_of_images

    def get_ids_of_frames_in_channel(self, channel: int) -> List[int]:
        connection = sqlite3.connect("my_database.db")
        cursor = connection.cursor()
        command = "SELECT Id FROM Images WHERE Channel = {0}".format(channel)
        ids = cursor.execute(command).fetchall()
        ids = [ids[i][0] for i in range(len(ids))]
        connection.close()
        return ids


class AppModel:
    def __init__(self, path_to_files: str):
        self.__solar_frames_storage = SolarFramesStorage(94, path_to_files)
        self.__viewport_transform = ViewportTransform()
        self.__time_line = TimeLine()
        self.__current_channel = CurrentChannel()
        self.__bezierMask = BezierMask()

        self.__observers = []

    def add_observer(self, in_observer):
        self.__observers.append(in_observer)

    def remove_observer(self, in_observer):
        self.__observers.remove(in_observer)

    def notify_observers(self):
        if self.__current_channel.current_channel_was_changed:
            channel_need_to_load = self.__current_channel.channel
            self.__solar_frames_storage.load_channel(channel_need_to_load)
        for x in self.__observers:
            x.modelIsChanged()

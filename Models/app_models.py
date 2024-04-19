import math
import os
import sqlite3
from typing import List
from enum import IntEnum, unique

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure, SubplotParams

import numpy as np
from PyQt5.QtCore import QPoint, QRect
import transformations
import sunpy.map
import sunpy.data.sample
import sunpy.visualization.colormaps.cm
from PyQt5.QtGui import QImage, QPixmap
from astropy.io import fits
import numpy.typing as npt

from result import SaverResults
from configuration import ConfigurationApp

from aiapy.calibrate import normalize_exposure, register, update_pointing

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
        im = QImage(canvas.buffer_rgba(), width, height, QImage.Format_RGBA8888)
        return im

# todo: Валидацию на корректное значение channel
class SolarFramesStorage:
    def __init__(self,
                 initial_channel: int,
                 path_to_directory: str,
                 viewport_transform: 'ViewportTransform',
                 configuration_app: 'ConfigurationApp'):
        self.__viewport_transform = viewport_transform
        self.__configuration_app: 'ConfigurationApp' = configuration_app
        self.__current_channel: int = initial_channel
        self.__path_to_directory: str = path_to_directory
        self.__loaded_channel: List[SolarFrame] = list()
        self.__initialize_database()
        self.cache_channel(initial_channel)

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
        print(files_in_directory)
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
        return self.__loaded_channel[index]

    def get_number_of_frames_in_current_channel(self) -> int:
        return len(self.__loaded_channel)
        #in_database = self.__get_number_of_frames_of_channel_in_database(self.__current_channel)
        #max_limit = self.__configuration_app.get_limit_for_channel(self.__current_channel)
        #return min(in_database, max_limit)

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
            border_point = point_at_t + QPoint(self.__width_in_pixels * normal_at_t.x() / magnitude_of_normal,
                                               self.__width_in_pixels * normal_at_t.y() / magnitude_of_normal)
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
        scale = self.__zoom * self.__origin_size_image
        scaled_solar_frame = solar_frame.qtimage.scaled(scale, scale)
        pixmap_for_draw = QPixmap.fromImage(scaled_solar_frame)
        return pixmap_for_draw

class TimeLine:
    def __init__(self, solar_frames_storage: SolarFramesStorage):
        self.__solar_frames_storage: SolarFramesStorage = solar_frames_storage
        self.__index_of_current_solar_frame: int = 0

    @property
    def index_of_current_solar_frame(self) -> int:
        return self.__index_of_current_solar_frame

    @index_of_current_solar_frame.setter
    def index_of_current_solar_frame(self, new_index) -> None:
        number_of_solar_frames_in_current_channel = self.__solar_frames_storage.get_number_of_frames_in_current_channel()
        if new_index >= number_of_solar_frames_in_current_channel:
            raise Exception("Index of current solar frame cannot be >= number of solar frames in current channel")

        self.__index_of_current_solar_frame = new_index

    @property
    def current_solar_frame(self) -> SolarFrame:
        i = self.__index_of_current_solar_frame
        return (self.__solar_frames_storage
                .get_solar_frame_by_index_from_current_channel(i))

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
    def current_frame_as_qpixmap(self) -> QPixmap:
        data = self.__frame.astype(np.uint8)
        qimage = QImage(data, self.__size, self.__size, self.__size, QImage.Format_Grayscale8)
        return QPixmap.fromImage(qimage)

    def animate_frame(self, delta_t: float):
        self.__t += delta_t
        self.__t = self.__validate_t_value(self.__t)
        self.__frame = self.__create_frame()
        self.__draw_line(self.__t, self.__frame)

    def get_frame_by_t(self, t: float):
        t = self.__validate_t_value(t)
        frame = self.__create_frame()
        self.__draw_line(t, frame)
        return frame

    def __validate_t_value(self, t: float) -> float:
        if t < 0:
            return 0
        elif t > 1:
            return 1
        else:
            return t

    def __draw_line(self, t, frame):
        if self.__direction == "horizontal":
            self.__draw_horizontal_line(t, frame)
        elif self.__direction == "vertical":
            self.__draw_vertical_line(t, frame)

    def __draw_horizontal_line(self, t, frame):
        start_border, end_border = self.__get_line_border_of_line(t)
        for i in range(start_border, end_border):
            frame[i] = 0

    def __draw_vertical_line(self, t, frame):
        start_border, end_border = self.__get_line_border_of_line(t)
        for i in range(start_border, end_border):
            frame.T[i] = 0

    def __create_frame(self):
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

    def __lininterp(self, p0: int, p1: int, t: float) -> int:
        return (1 - t) * p0 + t * p1

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

class Cubedata:
    def __init__(self, x_size: int, y_size: int):
        self.__x_size = x_size
        self.__y_size = y_size
        self.__frames: List = list()

    def add_frame(self, frame: npt.NDArray):
        if not frame.shape[1] == self.__y_size:
            raise Exception(f"Dont match y size of cubedata and frame. [{frame.shape[1]}] [{self.__y_size}]")

        if not frame.shape[0] == self.__x_size:
            raise Exception(f"Dont match x size of cubedata and frame. [{frame.shape[0]}] [{self.__x_size}]")

        self.__frames.append(frame)

    @property
    def number_of_frames(self) -> int:
        return len(self.__frames)

    @classmethod
    def create_from_debug_data(cls):
        cubedata = cls(600, 600)
        animated_frame = TestAnimatedFrame("horizontal", 30, 600)
        number_of_steps = 100
        t_values = [i/number_of_steps for i in range(number_of_steps)]
        for t in t_values:
            frame = animated_frame.get_frame_by_t(t)
            cubedata.add_frame(frame)

class TimeDistancePlot:
    def __init__(self, bezier_mask: BezierMask):
        pass

class AppModel:
    def __init__(self, path_to_files: str, path_to_export_result):
        initial_channel = 171
        self.__configaration = ConfigurationApp()
        self.__viewport_transform = ViewportTransform()
        self.__solar_frames_storage = SolarFramesStorage(initial_channel,
                                                         path_to_files,
                                                         self.__viewport_transform,
                                                         self.__configaration)
        self.__time_line = TimeLine(self.__solar_frames_storage)
        self.__current_channel = CurrentChannel(self.__solar_frames_storage, initial_channel)
        self.__bezier_mask = BezierMask()
        self.__interesting_solar_region = InterestingSolarRegion()
        self.__saver_results = SaverResults(self, path_to_export_result)
        self.__test_animated_frame = TestAnimatedFrame("horizontal", 30, 600)
        self.__selected_preview_mode = SelectedPreviewMode()

        self.__observers = []

    @property
    def saver_results(self) -> SaverResults:
        return self.__saver_results

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
        return self.__configaration

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


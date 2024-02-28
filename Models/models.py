import math
from typing import List
from PyQt5.QtCore import QPoint
import transformations


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
        image_pixel = transformations.transformPointFromViewToImage(viewport_pixel,
                                                                  [600, 600],
                                                                  [4096, 4096],
                                                                  self.__zoom,
                                                                  self.__offset)
        return image_pixel

    def transform_from_image_pixel_to_viewport_pixel(self, image_pixel: QPoint) -> QPoint:
        viewport_pixel = transformations.transformPointFromImageToView(image_pixel,
                                                                       [600, 600],
                                                                       [4096, 4096],
                                                                       self.__zoom,
                                                                       self.__offset)
        return viewport_pixel

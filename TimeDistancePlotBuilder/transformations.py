from typing import Union
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage


def transform_point_from_bezier_mask_to_solar_view(position_of_zone_interesting: QPoint,
                                                   point_in_bezier_mask: QPoint,
                                                   size_of_zone_interesting: int,
                                                   widget_size: int) -> QPoint:
    z_1: QPoint = QPoint(int(widget_size / 2 - 1), int(widget_size / 2 - 1))
    z_2: QPoint = position_of_zone_interesting
    p_1: QPoint = point_in_bezier_mask
    s_2: int = size_of_zone_interesting
    ws: int = widget_size

    p_2x = int( z_2.x() + ( p_1.x() - z_1.x() ) * (s_2 / ws) )
    p_2y = int( z_2.y() + ( p_1.y() - z_1.y() ) * (s_2 / ws) )
    
    return QPoint(p_2x, p_2y)
  
  
def transform_point_from_solar_view_to_bezier_mask(position_of_zone_interesting: QPoint,       
                                                   point_in_solar_view: QPoint,
                                                   size_of_zone_interesting: int,
                                                   widget_size: int) -> QPoint:
    z_1: QPoint = QPoint(int(widget_size / 2 - 1), int(widget_size / 2 - 1))
    z_2: QPoint = position_of_zone_interesting
    p_2: QPoint = point_in_solar_view
    ws: int = widget_size
    s_2: int = size_of_zone_interesting

    p_1x = ( ( p_2.x() - z_2.x() ) * ws ) / s_2 + z_1.x()
    p_1y = ( ( p_2.y() - z_2.y() ) * ws ) / s_2 + z_1.y()

    return QPoint(p_1x, p_1y)

def transform_point_from_solar_view_to_fits(point_in_solar_view: QPoint,
                                            offset: QPoint,
                                            size_of_fits: int,
                                            widget_size: int,
                                            zoom: float) -> QPoint:
    p_2: QPoint = point_in_solar_view
    s_3: int = size_of_fits
    ws: int = widget_size

    p_3x = int( ( p_2.x() - offset.x() ) * (s_3 / (ws * zoom)) ) 
    p_3y = int( ( p_2.y() - offset.y() ) * (s_3 / (ws * zoom)) )
    
    p_3y = s_3 - 1 - p_3y

    return QPoint(p_3x, p_3y)


# todo: need to test and fix !
def transform_point_from_fits_to_solar_view(point_in_fits: QPoint,
                                            offset: QPoint,
                                            size_of_fits: int,
                                            widget_size: int,
                                            zoom: float) -> QPoint:
    p_3: QPoint = point_in_fits
    s_3: int = size_of_fits
    ws: int = widget_size

    p_2x = int( p_3.x() * (ws * zoom / s_3) + offset.x() )
    p_2y = int( p_3.y() * (ws * zoom / s_3) + offset.y() )

    return QPoint(p_2x, p_2y)


# todo: Перенести эти функции в TransformViewport, только он их будет использовать
def transform_point_from_view_to_image(point_in_view: QPoint,
                                       size_of_view_in_pixels: Union[int, int],
                                       size_of_image_in_pixels: Union[int, int],
                                       zoom: float,
                                       offset: QPoint = QPoint(0, 0)) -> QPoint:
    if not size_of_view_in_pixels[0] == size_of_view_in_pixels[1]:
        raise Exception("View must be squared")

    if not size_of_image_in_pixels[0] == size_of_image_in_pixels[1]:
        raise Exception("Image must be squared")

    image_side_size_in_pixels = size_of_image_in_pixels[0]
    view_side_size_in_pixels = size_of_view_in_pixels[0]
    ratio = image_side_size_in_pixels / (zoom * view_side_size_in_pixels)

    return QPoint(int((point_in_view.x() - offset.x()) * ratio), int((point_in_view.y() - offset.y()) * ratio))


def transform_point_from_image_to_view(point_in_image: QPoint,
                                       size_of_view_in_pixels: (int, int),
                                       size_of_image_in_pixels: (int, int),
                                       zoom: float,
                                       offset: QPoint = QPoint(0, 0)) -> QPoint:
    if not size_of_view_in_pixels[0] == size_of_view_in_pixels[1]:
        raise Exception("View must be squared")

    if not size_of_image_in_pixels[0] == size_of_image_in_pixels[1]:
        raise Exception("Image must be squared")

    image_side_size_in_pixels = size_of_image_in_pixels[0]
    view_side_size_in_pixels = size_of_view_in_pixels[0]
    ratio = image_side_size_in_pixels / (zoom * view_side_size_in_pixels)
    return QPoint(int(point_in_image.x() / ratio + offset.x()), int(point_in_image.y() / ratio + offset.y()))


def transform_rectangle_into_square(top_left_point: QPoint,
                                    bottom_right: QPoint) -> (QPoint, QPoint):
    x_side_size = bottom_right.x() - top_left_point.x()
    y_side_size = bottom_right.y() - top_left_point.y()
    side_size_of_square = (x_side_size + y_side_size)/2
    top_left_point_of_square = top_left_point
    bottom_right_of_square = QPoint(top_left_point_of_square.x() + side_size_of_square,
                                 top_left_point_of_square.y() + side_size_of_square)
    return (top_left_point_of_square, bottom_right_of_square)

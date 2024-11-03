from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage

# todo: Перенести эти функции в TransformViewport, только он их будет использовать
def transform_point_from_view_to_image(point_in_view: QPoint,
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

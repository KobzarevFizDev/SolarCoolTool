from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage

# TODO: Переменовать. Эта функция принимает точку в пикселях экрана
# и преобразует ее в пиксель изображения (переобразование координат )
# SizeOfQuadInPixels - длина стороны квадратного виджета на котором отображается изображение

def transformPointFromViewToImage(pointInView: QPoint,
                                  sizeOfViewInPixels: (int, int),
                                  sizeOfImageInPixels: (int, int),
                                  zoom: float,
                                  offset: QPoint = QPoint(0, 0)) -> QPoint:
    if not sizeOfViewInPixels[0] == sizeOfViewInPixels[1]:
        raise Exception("View must be squared")

    if not sizeOfImageInPixels[0] == sizeOfImageInPixels[1]:
        raise Exception("Image must be squared")

    imageSideSizeInPixels = sizeOfImageInPixels[0]
    viewSideSizeInPixels = sizeOfViewInPixels[0]
    ratio = imageSideSizeInPixels / (zoom * viewSideSizeInPixels)

    return QPoint(int((pointInView.x() - offset.x()) * ratio), int((pointInView.y() - offset.y()) * ratio))

# TODO: Эта функция неработает корректно
def transformPointFromImageToView(pointInImage: QPoint,
                                  sizeOfViewInPixels: (int, int),
                                  sizeOfImageInPixels: (int, int),
                                  zoom: float,
                                  offset: QPoint = QPoint(0, 0)) -> QPoint:
    if not sizeOfViewInPixels[0] == sizeOfViewInPixels[1]:
        raise Exception("View must be squared")

    if not sizeOfImageInPixels[0] == sizeOfImageInPixels[1]:
        raise Exception("Image must be squared")

    imageSideSizeInPixels = sizeOfImageInPixels[0]
    viewSideSizeInPixels = sizeOfViewInPixels[0]
    ratio = imageSideSizeInPixels / (zoom * viewSideSizeInPixels)
    return QPoint(int(pointInImage.x() / ratio + offset.x()), int(pointInImage.y() / ratio + offset.y()))

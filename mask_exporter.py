from typing import TYPE_CHECKING, List
from PIL import Image
import numpy as np
from transformations import transformPointFromViewToImage
from PyQt5.QtCore import QPoint

if TYPE_CHECKING:
    from Models.solar_editor_model import SolarEditorModel

# todo: класс должен содержить метод, возращающий содержащий прямоугольник
class TrianglePolygon:
    def __init__(self, a: QPoint, b: QPoint, c: QPoint):
        self.__a: QPoint = a
        self.__b: QPoint = b
        self.__c: QPoint = c
        self.__topLeftBoundixBox, self.__bottomRightBoundingBox = self.__getBoundingBox()

    def __str__(self):
        return ("Triangle polygon: ({0} {1}) ({2} {3}) ({4} {5})"
                .format(self.__a.x(), self.__a.y(), self.__b.x(), self.__b.y(), self.__c.x(), self.__c.y()))

    @property
    def boundingBox(self) -> (QPoint, QPoint):
        return (self.__topLeftBoundixBox, self.__bottomRightBoundingBox)

    def __getBoundingBox(self) -> (QPoint, QPoint):
        topLeft = QPoint(min(self.__a.x(), self.__b.x(), self.__c.x()),
                         max(self.__a.y(), self.__b.y(), self.__c.y()))

        bottomRight = QPoint(max(self.__a.x(), self.__b.x(), self.__c.x()),
                             min(self.__a.y(), self.__b.y(), self.__c.y()))

        return (topLeft, bottomRight)

    def isInTriangle(self, p: QPoint) -> bool:
        a, b, c = self.__a, self.__b, self.__c
        aSide = (a.y() - b.y())*p.x() + (b.x() - a.x()) * p.y() + (a.x()*b.y() - b.x()*a.y())
        bSide = (b.y() - c.y())*p.x() + (c.x() - b.x()) * p.y() + (b.x()*c.y() - c.x()*b.y())
        cSide = (c.y() - a.y())*p.x() + (a.x() - c.x()) * p.y() + (c.x()*a.y() - a.x()*c.y())
        return (aSide >= 0 and bSide >= 0 and cSide >= 0) or (aSide < 0 and bSide < 0 and cSide < 0)


class MaskExporter:
    def __init__(self, solarEditorModel):
        self.__solarEditorModel: SolarEditorModel = solarEditorModel

    def __triangulateMask(self) -> List[TrianglePolygon]:
        topBorder: List[QPoint] = self.__solarEditorModel.maskSpline.getPointsOfTopBorder()
        bottomBorder: List[QPoint] = self.__solarEditorModel.maskSpline.getPointsOfBottomBorder()

        zoom = self.__solarEditorModel.solarViewModel.zoom
        offset = self.__solarEditorModel.solarViewModel.offset

        topBorder: List[QPoint] = [transformPointFromViewToImage(p, (600, 600), (4096, 4096), zoom, offset) for p in topBorder]
        bottomBorder: List[QPoint] = [transformPointFromViewToImage(p, (600, 600), (4096, 4096), zoom, offset) for p in bottomBorder]

        numberOfRectangePolygon = len(topBorder) - 1
        trianglePolygons: List[TrianglePolygon] = list()
        for i in range(numberOfRectangePolygon):
            a = topBorder[i]
            b = topBorder[i + 1]
            c = bottomBorder[i]
            upTrianglePolygon: TrianglePolygon = TrianglePolygon(a, b, c)
            trianglePolygons.append(upTrianglePolygon)

            a = bottomBorder[i]
            b = bottomBorder[i + 1]
            c = topBorder[i + 1]
            bottomTrianglePolygon: TrianglePolygon = TrianglePolygon(a, b, c)
            trianglePolygons.append(bottomTrianglePolygon)


        return trianglePolygons

    def __rasterizeMask(self, outputMask, polygons: List[TrianglePolygon]):
        for polygon in polygons:
            self.__rasterizePolygon(outputMask, polygon)

    def __rasterizePolygon(self, outputMask, polygon: TrianglePolygon):
        topLeft, bottomRight = polygon.boundingBox
        for x in range(topLeft.x(), bottomRight.x()):
            for y in range(bottomRight.y(), topLeft.y()):
                p = QPoint(x, y)

                if polygon.isInTriangle(p):
                    outputMask[y][x] = 255


    def exportToBmp(self, pathToExport):
        outputMask = np.zeros((4096, 4096), dtype=np.uint8)
        trianglePolygons = self.__triangulateMask()
        for trianglePolygon in trianglePolygons:
            self.__rasterizePolygon(outputMask, trianglePolygon)
        bmpMask = Image.fromarray(outputMask, "L")
        bmpMask.save(pathToExport)

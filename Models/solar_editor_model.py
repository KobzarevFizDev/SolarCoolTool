import math
from typing import List

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage
from scipy.interpolate import CubicSpline

from images_indexer import ImagesIndexer
from transformations import (transformPointFromViewToImage,
                             transformPointFromImageToView,
                             transformRectangeIntoSquare)


class CurveAreaSegment:
    def __init__(self, topRight, topLeft, bottomRight, bottomLeft):
        self.topRight = topRight
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        self.bottomLeft = bottomLeft

    def __eq__(self, other: 'AreaSegment'):
        return self.topRight == other.topRight and \
               self.topLeft == other.topLeft and \
               self.bottomRight == other.bottomRight and \
               self.bottomLeft == other.bottomLeft


class SolarViewModel:
    def __init__(self, indexer: ImagesIndexer):
        self.__imagesIndexer = indexer
        self.__originImageScale = 600
        self.__zoom = 1
        self.__offset: QPoint = QPoint(0,0)

        self.__sizeOfImageInPixels: (int, int) = (4096, 4096)
        self.__sizeOfViewInPixels: (int, int) = (600, 600)

        self.__topLeftPointInImage: QPoint = QPoint(-1, -1)
        self.__bottomRightPointInImage: QPoint = QPoint(-1, -1)

    # TODO: Подумать нужны ли свойства в данном случае
    @property
    def originImageScale(self):
        return self.__originImageScale

    @property
    def zoom(self):
        return self.__zoom

    @property
    def offset(self):
        return self.__offset

    @property
    def selectedPlotInView(self) -> (QPoint, QPoint):
        topLeftPointInView = transformPointFromImageToView(self.__topLeftPointInImage,
                                                           self.__sizeOfViewInPixels,
                                                           self.__sizeOfImageInPixels,
                                                           self.__zoom,
                                                           self.__offset)
        bottomRightPointInView = transformPointFromImageToView(self.__bottomRightPointInImage,
                                                               self.__sizeOfViewInPixels,
                                                               self.__sizeOfImageInPixels,
                                                               self.__zoom,
                                                               self.__offset)
        return (topLeftPointInView, bottomRightPointInView)

    def selectPlotOfImage(self,
                          topLeftPointInView: QPoint,
                          bottomRightPointInView: QPoint) -> None:
        topLeftPointInView, bottomRightPointInView = transformRectangeIntoSquare(topLeftPointInView, bottomRightPointInView)
        self.__topLeftPointInImage = transformPointFromViewToImage(topLeftPointInView,
                                                                   self.__sizeOfViewInPixels,
                                                                   self.__sizeOfImageInPixels,
                                                                   self.__zoom,
                                                                   self.__offset)


        self.__bottomRightPointInImage = transformPointFromViewToImage(bottomRightPointInView,
                                                                       self.__sizeOfViewInPixels,
                                                                       self.__sizeOfImageInPixels,
                                                                       self.__zoom,
                                                                       self.__offset)

    def setOriginSolarPreviewImage(self, originImageScale):
        self.__originImageScale = originImageScale

    def changeOffsetSolarPreviewImage(self, deltaOffset):
        self.__offset += deltaOffset

    def changeZoom(self, deltaZoom):
        self.__zoom += deltaZoom


class TimeLineModel:
    def __init__(self, indexer: ImagesIndexer):
        self.__imagesIndexer = indexer
        self.indexImage = 0

    def setIndexImage(self, index):
        self.indexImage = index


class CurrentChannelModel:
    def __init__(self, indexer: ImagesIndexer):
        self.__imagesIndexer = indexer
        self.__currentChannel = 94
        self.__availableChannels = []
        self.__notAvailableChannels = []
        self.__checkAvailableChannels()
        self.__newChannelWasSelected = True
        self.__imagesIndexer.cacheChannel(self.__currentChannel)

    @property
    def newChannelWasSelected(self) -> bool:
        res: bool = self.__newChannelWasSelected
        self.__newChannelWasSelected = False
        return res

    @property
    def currentChannel(self) -> int:
        return self.__currentChannel

    @property
    def availableChannels(self) -> List[int]:
        return self.__availableChannels

    @property
    def notAvailableChannels(self) -> List[int]:
        return self.__notAvailableChannels

    @property
    def numberOfImagesInChannel(self) -> int:
        return self.__imagesIndexer.getCountImagesInChannel(self.__currentChannel)

    def setCurrentChannel(self, channel):
        availableChannels = [94, 131, 171, 193, 211, 355]
        if not channel in availableChannels:
            raise Exception("Incorrect channel: {0}".format(channel))
        else:
            self.__newChannelWasSelected = self.__currentChannel != channel
            self.__currentChannel = channel

    def __checkAvailableChannels(self):
        # TODO: Зачем создавать indexer если он уже создан в __init__?
        indexer = ImagesIndexer("C:\\SolarImages")

        channels = [94, 131, 171, 193, 211, 355]
        for i, channel in enumerate(channels):
            if indexer.isExistImagesInChannel(channel):
                print("A{0} is available".format(channel))
                self.__availableChannels.append(channel)
            else:
                print("A{0} is not available".format(channel))
                self.__notAvailableChannels.append(channel)


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

    def pointAtT(self, t) -> QPoint:
        A = (1-t)**3 * self.__p0
        B = 3 * (1-t)**2 * t * self.__p1
        C = 3 * (1-t)*t**2 * self.__p2
        D = t**3 * self.__p3

        return A + B + C + D

    def tangentAtT(self, t) -> QPoint:
        A = 3 * (1-t)**2 * (self.__p1 - self.__p0)
        B = 6 * (1 - t) * t * (self.__p2 - self.__p1)
        C = 3 * t**2 * (self.__p3 - self.__p2)
        return A + B + C

    def normalAtT(self, t) -> QPoint:
        tangent = self.tangentAtT(t)
        return QPoint(tangent.y(), -tangent.x())

class MaskSplineModel:
    def __init__(self):
        self.__numberOfSegments: int = 10
        self.__firstAnchor: QPoint = QPoint(-1, -1)
        self.__widthOfMask: int = 30
        defaultBezierCurve = BezierCurve(QPoint(100, 100),
                                         QPoint(200, 200),
                                         QPoint(300, 150),
                                         QPoint(400, 300))
        self.__curves: List[BezierCurve] = [defaultBezierCurve,]

    # Значит есть что рисовать (отображать)
    @property
    def isAvailableToDraw(self) -> bool:
        return len(self.__curves) > 0

    # TODO: Переименовать (количество состовляющих кривых)
    @property
    def numberOfCurves(self):
        return len(self.__curves)

    def addAnchor(self, anchor: QPoint):
        if self.__firstAnchor == QPoint(-1, -1):
            self.__firstAnchor = anchor
        else:
            distanceBetweenPointsAlongXAxis = anchor.x() - self.__firstAnchor.x()
            stepByXAxis = distanceBetweenPointsAlongXAxis / 3
            stepByYAxis = 20
            p0 = self.__firstAnchor
            p1 = QPoint(p0.x() + stepByXAxis, p0.y() + stepByYAxis)
            p2 = QPoint(p1.x() + stepByXAxis, p0.y() - stepByYAxis)
            p3 = anchor
            bezierCurve = BezierCurve(p0, p1, p2, p3)
            self.__curves.append(bezierCurve)

    def removeLastAnchor(self):
        if len(self.__curves) == 0:
            return
        else:
            self.__curves.remove(self.__curves[len(self.__curves)-1])

    # TODO: Индексатор
    # TODO: Это приватный метод
    def getCurveAtIndex(self, index) -> BezierCurve:
        return self.__curves[index]

    # TODO: Дублирование вычислений
    def getPointsOfBottomBorder(self) -> List[QPoint]:
        pointsOfBottomBorder: List[QPoint] = list()
        for i in range(self.numberOfCurves):
            bezierCurve: BezierCurve = self.getCurveAtIndex(i)
            for j in range(self.__numberOfSegments + 1):
                t = j * 1 / self.__numberOfSegments
                point: QPoint = bezierCurve.pointAtT(t)
                pointsOfBottomBorder.append(point)
        return pointsOfBottomBorder


    def getPointsOfTopBorder(self) -> List[QPoint]:
        pointsOfTopBorder: List[QPoint] = list()
        for i in range(self.numberOfCurves):
            bezierCurve: BezierCurve = self.getCurveAtIndex(i)
            for j in range(self.__numberOfSegments + 1):
                t = j * 1 / self.__numberOfSegments
                normal: QPoint = bezierCurve.normalAtT(t)
                magnitudeOfNormal = math.sqrt(normal.x() ** 2 + normal.y() ** 2)
                finishPoint = bezierCurve.pointAtT(t) + QPoint(self.__widthOfMask * normal.x()/magnitudeOfNormal, self.__widthOfMask * normal.y()/magnitudeOfNormal)
                pointsOfTopBorder.append(finishPoint)
        return pointsOfTopBorder

    def increaseNumberOfSegments(self):
        self.__numberOfSegments += 1

    def decreaseNumberOfSegments(self):
        if self.__numberOfSegments > 3:
            self.__numberOfSegments -= 1



#TODO: Устаревшее
class CurveModel:
    def __init__(self, indexer: ImagesIndexer):
        self.__imagesIndexer = indexer
        self.numberOfSegments = 10
        self.points = list()

    @property
    def numberOfPoints(self):
        return len(self.points)

    def addPoint(self, point):
        self.points.append(point)
        if self.numberOfPoints > 3:
            self.rebuildSpline()

    def removePoint(self, point):
        self.points.remove(point)
        if self.numberOfPoints > 3:
            self.rebuildSpline()

    def increaseNumberOfCurveSegments(self):
        self.numberOfSegments += 1

    def decreaseNumberOfCurveSegments(self):
        if self.numberOfSegments > 3:
            self.numberOfSegments -= 1

    def getPoints(self):
        return self.points

    def rebuildSpline(self):
        x = self.__get_x_values()
        y = self.__get_y_values()
        self.x0 = min(x)
        self.xn = max(x)
        self.spline = CubicSpline(x, y)

    def getPoint(self, t):
        x = self.__get_x_by_t(t)
        return QPoint(x, int(self.spline(x)))

    def __get_x_values(self):
        return [point.x for point in self.points]

    def __get_y_values(self):
        return [point.y for point in self.points]

    def __get_x_by_t(self, t):
        return self.x0 + (self.xn - self.x0) * t


class SolarEditorModel:
    def __init__(self, indexer: ImagesIndexer):
        self.__imagesIndexer = indexer
        self.__observers = []
        self.__curveModel = CurveModel(indexer)
        self.__solarViewModel = SolarViewModel(indexer)
        self.__timeLineModel = TimeLineModel(indexer)
        self.__currentChannelModel = CurrentChannelModel(indexer)
        self.__maskSpline = MaskSplineModel()


    @property
    def curveModel(self):
        return self.__curveModel

    @property
    def solarViewModel(self):
        return self.__solarViewModel

    @property
    def timeLineModel(self):
        return self.__timeLineModel

    @property
    def currentChannelModel(self):
        return self.__currentChannelModel

    @property
    def maskSpline(self) -> MaskSplineModel:
        return self.__maskSpline

    @property
    def currentSolarImage(self) -> QImage:
        channel = self.__currentChannelModel.currentChannel
        indexOfImage = self.__timeLineModel.indexImage
        return self.__imagesIndexer.getImageInChannelByIndex(indexOfImage)

    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObservers(self):
        if self.__currentChannelModel.newChannelWasSelected:
            self.__imagesIndexer.cacheChannel(self.__currentChannelModel.currentChannel)

        for x in self.__observers:
            x.modelIsChanged()

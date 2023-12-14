from typing import List

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage
from scipy.interpolate import CubicSpline

from images_indexer import ImagesIndexer


class CurvePoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.r = 10
        self.w = 1
        self.color = Qt.red

    def changePosition(self, deltaX: int, deltaY: int):
        self.x += deltaX
        self.y += deltaY

    def highlightThisPointAsSelected(self):
        self.color = Qt.blue

    def unhightlightThisPointAsSelected(self):
        self.color = Qt.red

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
    def currentSolarImage(self) -> QImage:
        channel = self.__currentChannelModel.currentChannel
        indexOfImage = self.__timeLineModel.indexImage
        return self.__imagesIndexer.getImageInChannelByIndex(indexOfImage)
        #return self.__imagesIndexer.getImage(channel, indexOfImage)

    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObservers(self):
        if self.__currentChannelModel.newChannelWasSelected:
            self.__imagesIndexer.cacheChannel(self.__currentChannelModel.currentChannel)

        for x in self.__observers:
            x.modelIsChanged()

from PyQt5.QtCore import Qt, QPoint
from scipy.interpolate import CubicSpline

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


# TODO: Выделить базовый класс для модели

class SolarViewModel:
    def __init__(self):
        self.__observers = []
        self.__originImageScale = 600
        self.__zoom = 1


    @property
    def originImageScale(self):
        return self.__originImageScale

    @property
    def zoom(self):
        return self.__zoom

    def setOriginSolarPreviewImage(self, originImageScale):
        self.__originImageScale = originImageScale
        self.notifyObservers()

    def changeZoom(self, deltaZoom):
        self.__zoom += deltaZoom
        self.notifyObservers()

    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObservers(self):
        for x in self.__observers:
            x.modelIsChanged()


class TimeLineModel:
    def __init__(self):
        self.__observers = []
        self.indexFrame = 0

    def setIndexFrame(self, index):
        self.indexFrame = index

    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObservers(self):
        for x in self.__observers:
            x.modelIsChanged()


class CurrentChannelModel:
    def __init__(self):
        self.__observers = []
        self.currentChannel = 94

    def setCurrentChannel(self, channel):
        availableChannels = [94, 131, 171, 193, 211, 355]
        if not channel in availableChannels:
            raise Exception("Incorrect channel: {0}".format(channel))
        else:
            self.currentChannel = channel


    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObservers(self):
        for x in self.__observers:
            x.modelIsChanged()

class CurveModel:
    def __init__(self):
        self.__observers = []
        self.numberOfSegments = 10
        self.points = list()

    @property
    def numberOfPoints(self):
        return len(self.points)

    def addPoint(self, point):
        self.points.append(point)
        if self.numberOfPoints > 3:
            self.rebuildSpline()
        self.notifyObservers()

    def removePoint(self, point):
        self.points.remove(point)
        if self.numberOfPoints > 3:
            self.rebuildSpline()
        self.notifyObservers()

    def increaseNumberOfCurveSegments(self):
        self.numberOfSegments += 1
        self.notifyObservers()

    def decreaseNumberOfCurveSegments(self):
        if self.numberOfSegments > 3:
            self.numberOfSegments -= 1
            self.notifyObservers()

    def getPoints(self):
        return self.points

    def rebuildSpline(self):
        x = self.__get_x_values()
        y = self.__get_y_values()
        self.x0 = min(x)
        self.xn = max(x)
        self.spline = CubicSpline(x, y)
        self.notifyObservers()

    def getPoint(self, t):
        x = self.__get_x_by_t(t)
        return QPoint(x, int(self.spline(x)))

    def __get_x_values(self):
        return [point.x for point in self.points]

    def __get_y_values(self):
        return [point.y for point in self.points]

    def __get_x_by_t(self, t):
        return self.x0 + (self.xn - self.x0) * t


    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObservers(self):
        for x in self.__observers:
            x.modelIsChanged()

class SolarEditorModel:
    def __init__(self):
        self.__curveModel = CurveModel()
        self.__solarViewModel = SolarViewModel()
        self.__timeLineModel = TimeLineModel()
        self.__currentChannelModel = CurrentChannelModel()


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

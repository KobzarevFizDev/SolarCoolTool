class SolarViewModel:
    def __init__(self):
        self.__observers = []
        self.zoom = 1
        self.originScaleImage = 600
        self.originImagePosition = (0, 0)

    def setOriginSolarPreviewImage(self, originScale):
        self.originScaleImage = originScale
        self.notifyObserver()

    def setOriginSolerPreviewImage(self, originImagePosition):
        self.originImagePosition = originImagePosition
        self.notifyObserver()

    def moveImage(self, deltaPosition):
        self.originImagePosition[0] += deltaPosition[0]
        self.originImagePosition[1] += deltaPosition[1]
        self.notifyObserver()

    def changeZoom(self, deltaZoom):
        self.zoom += deltaZoom
        self.notifyObserver()

    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObserver(self):
        for x in self.__observers:
            x.modelIsChanged()
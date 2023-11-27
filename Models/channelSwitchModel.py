class ChannelSwitchModel:
    def __init__(self):
        self.__observers = []
        self.channel:int = 94

    def addObserver(self, inObserver):
        self.__observers.append(inObserver)

    def removeObserver(self, inObserver):
        self.__observers.remove(inObserver)

    def notifyObserver(self):
        for x in self.__observers:
            x.modelIsChanged()
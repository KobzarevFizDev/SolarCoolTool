
class NotFoundConfigurationPropertyWithName(Exception):
    def __init__(self, property_name: str) -> None:
        self.__property_name = property_name

    def __str__(self) -> str:
        return "Not founded property with name = {0} in configuration.txt".format(self.__property_name)
    

class IncorrectZoneInterestingSize(Exception):
    def __init__(self, size: int) -> None:
        self.__size = size

    def __str__(self) -> str:
        return "Incorrect zone interesting size. Size = {0}".format(self.__size)
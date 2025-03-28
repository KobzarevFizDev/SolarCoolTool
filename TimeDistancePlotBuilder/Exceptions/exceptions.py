
class NotFoundConfigurationPropertyWithName(Exception):
    def __init__(self, property_name: str) -> None:
        self.__property_name = property_name

    def __str__(self) -> str:
        return "Not founded property with name = {0} in configuration.txt".format(self.__property_name)
    
class ConfigKeyValueError(Exception):
    def __init__(self, property_name: str) -> None:
        self.__property_name = property_name

    def __str__(self):
        return "Syntax error with property = {0} in configuration.txt".format(self.__property_name)
    
class ConfigValueError(Exception):
    def __init__(self, property_name: str) -> None:
        self.__property_name = property_name
    
    def __str__(self):
        return "Incorrect value for property = {0} in configuration.txt".format(self.__property_name)

class IncorrectZoneInterestingSize(Exception):
    def __init__(self, size: int) -> None:
        self.__size = size

    def __str__(self) -> str:
        return "Incorrect zone interesting size. Size = {0}".format(self.__size)
    

class IncorrectPath(Exception):
    def __init__(self, path: str) -> None:
        self.__path = path

    def __str__(self) -> str:
        return "Incorrect path. Path = {0}".format(self.__path)
    
class FileNameIsEmpty(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Filename is empty"
    
class NotFoundDataForExport(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Not found data for export"

class DataForExportNotValid(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Data for export is not valid"
    
class DataNotLoaded(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Cannot access to unloading data"
    
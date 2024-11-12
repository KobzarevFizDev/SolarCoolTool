class NotFoundConfigurationPropertyWithName(Exception):
    def __init__(self, property_name: str):
        self.__property_name = property_name

    def __str__(self) -> str:
        return "Not founded property with name = {0} in configuration.txt".format(self.__property_name)
from TimeDistancePlotBuilder.Exceptions.exceptions import NotFoundConfigurationPropertyWithName


STEP_FOR_A94_PROPERTY_NAME = "STEP_FOR_A94"
STEP_FOR_A131_PROPERTY_NAME = "STEP_FOR_A131"
STEP_FOR_A171_PROPERTY_NAME = "STEP_FOR_A171"
STEP_FOR_A193_PROPERTY_NAME = "STEP_FOR_A193"
STEP_FOR_A211_PROPERTY_NAME = "STEP_FOR_A211"
STEP_FOR_A304_PROPERTY_NAME = "STEP_FOR_A304"
STEP_FOR_A335_PROPERTY_NAME = "STEP_FOR_A335"

MAX_NUMBER_OF_FRAMES_A94_PROPERTY_NAME = "MAX_NUMBER_OF_FRAMES_A94"
MAX_NUMBER_OF_FRAMES_A131_PROPERTY_NAME = "MAX_NUMBER_OF_FRAMES_A131"
MAX_NUMBER_OF_FRAMES_A171_PROPERTY_NAME = "MAX_NUMBER_OF_FRAMES_A171"
MAX_NUMBER_OF_FRAMES_A193_PROPERTY_NAME = "MAX_NUMBER_OF_FRAMES_A193"
MAX_NUMBER_OF_FRAMES_A211_PROPERTY_NAME = "MAX_NUMBER_OF_FRAMES_A211"
MAX_NUMBER_OF_FRAMES_A304_PROPERTY_NAME = "MAX_NUMBER_OF_FRAMES_A304"
MAX_NUMBER_OF_FRAMES_A335_PROPERTY_NAME = "MAX_NUMBER_OF_FRAMES_A335"

PATH_TO_SOLAR_IMAGES_PROPERTY_NAME = "PATH_TO_SOLAR_IMAGES"
PATH_TO_EXPORT_PROPERTY_NAME = "PATH_TO_EXPORT"

INITIAL_CHANNEL = "INITIAL_CHANEL"

class ConfigurationApp:
    def __init__(self, path_to_configuration: str):
        self.__path_to_configuration: str = path_to_configuration

    def get_step_for_channel(self, channel: int) -> int:
        return {94:self.step_for_channel_a94,
                131:self.step_for_channel_a131,
                171:self.step_for_channel_a171,
                193:self.step_for_channel_a193,
                211:self.step_for_channel_a211,
                304:self.step_for_channel_a304,
                335:self.step_for_channel_a335}[channel]


    def get_limit_for_channel(self, channel: int) -> int:
        return {94:self.max_number_of_frames_in_a94,
                131:self.max_number_of_frames_in_a131,
                171:self.max_number_of_frames_in_a171,
                193:self.max_number_of_frames_in_a193,
                211:self.max_number_of_frames_in_a211,
                304:self.max_number_of_frames_in_a304,
                335:self.max_number_of_frames_in_a335}[channel]

    @property
    def max_number_of_frames_in_a94(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(MAX_NUMBER_OF_FRAMES_A94_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def max_number_of_frames_in_a131(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(MAX_NUMBER_OF_FRAMES_A131_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def max_number_of_frames_in_a171(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(MAX_NUMBER_OF_FRAMES_A171_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def max_number_of_frames_in_a193(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(MAX_NUMBER_OF_FRAMES_A193_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def max_number_of_frames_in_a211(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(MAX_NUMBER_OF_FRAMES_A211_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def max_number_of_frames_in_a304(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(MAX_NUMBER_OF_FRAMES_A304_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def max_number_of_frames_in_a335(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(MAX_NUMBER_OF_FRAMES_A335_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)


    @property
    def step_for_channel_a94(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(STEP_FOR_A94_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)


    @property
    def step_for_channel_a94(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(STEP_FOR_A94_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)


    @property
    def step_for_channel_a131(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(STEP_FOR_A131_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def step_for_channel_a171(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(STEP_FOR_A171_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def step_for_channel_a193(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(STEP_FOR_A193_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def step_for_channel_a211(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(STEP_FOR_A211_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def step_for_channel_a304(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(STEP_FOR_A304_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    

    @property
    def step_for_channel_a335(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(STEP_FOR_A335_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)

    @property
    def path_to_solar_images(self) -> str:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(PATH_TO_SOLAR_IMAGES_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return property_value


    @property
    def path_to_export_results(self) -> str:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(PATH_TO_EXPORT_PROPERTY_NAME)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return property_value
    
    @property
    def initial_channel(self) -> int:
        line_with_property: str = self.__get_line_with_property_from_configuration_file_by_property_name(INITIAL_CHANNEL)
        property_value: str = self.__get_property_value_from_line(line_with_property)
        return int(property_value)
    
    def __get_property_value_from_line(self, line_with_property: str) -> str:
        start_index: int = line_with_property.index('[') + 1
        finish_index: int = line_with_property.index(']')
        value: str = line_with_property[start_index : finish_index]
        return value


    def __get_line_with_property_from_configuration_file_by_property_name(self, property_name: str) -> str:
        with open(self.__path_to_configuration) as f:
            line_with_path: str = None
            for line in f.readlines():
                if property_name in line:
                    line_with_path = line
            
            if line_with_path == None:
                raise NotFoundConfigurationPropertyWithName(property_name)
            else:
                return line_with_path
            
    def __str__(self):
        return (f"step_for_a94 = {self.__step_for_a94}, "
                f"step_for_a131 = {self.__step_for_a131}, "
                f"step_for_a171 = {self.__step_for_a171}, "
                f"step_for_a193 = {self.__step_for_a193}, "
                f"step_for_a211 = {self.__step_for_a211}, "
                f"step_for_a304 = {self.__step_for_a304}, "
                f"step_for_a335 = {self.__step_for_a335}, "
                f"max_number_of_frames_a94 = {self.__max_number_of_frames_in_a94}, "
                f"max_number_of_frames_a131 = {self.__max_number_of_frames_in_a131}, "
                f"max_number_of_frames_a171 = {self.__max_number_of_frames_in_a171}, "
                f"max_number_of_frames_a211 = {self.__max_number_of_frames_in_a211}, "
                f"max_number_of_frames_a304 = {self.__max_number_of_frames_in_a304}, "
                f"max_number_of_frames_a335 = {self.__max_number_of_frames_in_a335}")


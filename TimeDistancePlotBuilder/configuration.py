class ConfigurationApp:
    def __init__(self):
        self.__step_for_a94: int = 1
        self.__step_for_a131: int = 1
        self.__step_for_a171: int = 1
        self.__step_for_a193: int = 1
        self.__step_for_a211: int = 1
        self.__step_for_a304: int = 1
        self.__step_for_a335: int = 1

        self.__max_number_of_frames_in_a94: int = 50
        self.__max_number_of_frames_in_a131: int = 50
        self.__max_number_of_frames_in_a171: int = 50
        self.__max_number_of_frames_in_a193: int = 50
        self.__max_number_of_frames_in_a211: int = 50
        self.__max_number_of_frames_in_a304: int = 50
        self.__max_number_of_frames_in_a355: int = 50

        self.__read_configuration_file()

    def get_step_for_channel(self, channel: int) -> int:
        return {94:self.__step_for_a94,
                131:self.__step_for_a131,
                171:self.__step_for_a171,
                193:self.__step_for_a193,
                211:self.__step_for_a211,
                304:self.__step_for_a304,
                335:self.__step_for_a335}[channel]

    def get_limit_for_channel(self, channel: int) -> int:
        return {94:self.__max_number_of_frames_in_a94,
                131:self.__max_number_of_frames_in_a131,
                171:self.__max_number_of_frames_in_a171,
                193:self.__max_number_of_frames_in_a193,
                211:self.__max_number_of_frames_in_a211,
                304:self.__max_number_of_frames_in_a304,
                335:self.__max_number_of_frames_in_a335}[channel]

    def __read_configuration_file(self) -> None:
        with open("./configuration.txt") as f:
            for line in f.readlines():
                if len(line) > 3:
                    splited = line.split('=')
                    key = splited[0]
                    value = splited[1]
                    self.__set_config_parametr(key, value)

    def __set_config_parametr(self, key: str, value: str) -> None:
        if not self.__is_correct_key_parametr(key):
            raise Exception(f"Key = '({key})' of config parametr not correct")
        if not self.__is_correct_value(value):
            raise Exception(f"Value = '({value})' of config parametr not correct")

        if key == "STEP_FOR_A94":
            self.__step_for_a94 = int(value)
        elif key == "STEP_FOR_A131":
            self.__step_for_a131 = int(value)
        elif key == "STEP_FOR_A171":
            self.__step_for_a171 = int(value)
        elif key == "STEP_FOR_A193":
            self.__step_for_a193 = int(value)
        elif key == "STEP_FOR_A211":
            self.__step_for_a211 = int(value)
        elif key == "STEP_FOR_A304":
            self.__step_for_a304 = int(value)
        elif key == "STEP_FOR_A335":
            self.__step_for_a335 = int(value)
        elif key == "MAX_NUMBER_OF_FRAMES_A94":
            self.__max_number_of_frames_in_a94 = int(value)
        elif key == "MAX_NUMBER_OF_FRAMES_A131":
            self.__max_number_of_frames_in_a131 = int(value)
        elif key == "MAX_NUMBER_OF_FRAMES_A171":
            self.__max_number_of_frames_in_a171 = int(value)
        elif key == "MAX_NUMBER_OF_FRAMES_A193":
            self.__max_number_of_frames_in_a193 = int(value)
        elif key == "MAX_NUMBER_OF_FRAMES_A211":
            self.__max_number_of_frames_in_a211 = int(value)
        elif key == "MAX_NUMBER_OF_FRAMES_A304":
            self.__max_number_of_frames_in_a304 = int(value)
        elif key == "MAX_NUMBER_OF_FRAMES_A335":
            self.__max_number_of_frames_in_a335 = int(value)


    def __is_correct_key_parametr(self, key: str) -> bool:
        key = key.replace("\n", '')
        correct_keys = ["STEP_FOR_A94",
                        "STEP_FOR_A131",
                        "STEP_FOR_A171",
                        "STEP_FOR_A193",
                        "STEP_FOR_A211",
                        "STEP_FOR_A304",
                        "STEP_FOR_A335",
                        "MAX_NUMBER_OF_FRAMES_A94",
                        "MAX_NUMBER_OF_FRAMES_A131",
                        "MAX_NUMBER_OF_FRAMES_A171",
                        "MAX_NUMBER_OF_FRAMES_A193",
                        "MAX_NUMBER_OF_FRAMES_A211",
                        "MAX_NUMBER_OF_FRAMES_A304",
                        "MAX_NUMBER_OF_FRAMES_A335"]

        return key in correct_keys

    def __is_correct_value(self, value: str) -> bool:
        value = value.replace("\n", '')
        return value.isdigit()

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

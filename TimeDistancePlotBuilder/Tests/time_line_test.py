from unittest import main, TestCase
from PyQt5.QtCore import QPoint
from Models.app_models import TimeLine

class TimeLineTest(TestCase):
    def setUp(self) -> None:
        self.__timeline = TimeLine()

    def test_set_correct_index(self) -> None:
        msg = "set correct index - fail"
        self.__timeline.number_of_solar_frames_in_current_channel = 100
        self.__timeline.index_of_current_solar_frame = 10
        expected_index = 10
        actual_index = self.__timeline.index_of_current_solar_frame
        self.assertEqual(expected_index, actual_index, msg)

    def test_set_incorrect_index(self) -> None:
        with self.assertRaises(Exception):
            msg = "set incorrect index - fail"
            self.__timeline.number_of_solar_frames_in_current_channel = 100
            self.__timeline.index_of_current_solar_frame = 110
            expected_index = 10
            actual_index = self.__timeline.index_of_current_solar_frame
            self.assertEqual(expected_index, actual_index, msg)

if __name__ == "__main__":
    main()

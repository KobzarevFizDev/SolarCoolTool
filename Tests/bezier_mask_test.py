from unittest import main, TestCase
from Models.models import BezierMask

class BezierMaskTest(TestCase):
    def test_increase_number_of_segments(self) -> None:
        msg = "increase_number_of_segments() not working"
        number_segments = 20
        bezier_mask = BezierMask(number_of_segments=number_segments)
        bezier_mask.increase_number_of_segments()
        expected = 21
        actual = bezier_mask.number_of_segments
        self.assertEqual(expected, actual, msg)

    def test_decrease_number_of_segments(self) -> None:
        msg = "decrease_number_of_segments() not working"
        number_segments = 20
        bezier_mask = BezierMask(number_of_segments=number_segments)
        bezier_mask.decrease_number_of_segments()
        expected = 19
        actual = bezier_mask.number_of_segments
        self.assertEqual(expected, actual, msg)

    def test_maximum_number_of_segments(self) -> None:
        msg = "max limit not working"
        number_segments = 20
        max_number_segments = 45
        bezier_mask = BezierMask(number_of_segments=number_segments,
                                 max_number_of_segments=max_number_segments)
        for i in range(100):
            bezier_mask.increase_number_of_segments()

        expected_number_of_segments = max_number_segments
        actual_number_of_segments = bezier_mask.number_of_segments
        self.assertEqual(expected_number_of_segments, actual_number_of_segments, msg)

    def test_minimum_number_of_segments(self) -> None:
        msg = "min limit not working"
        number_segments = 20
        min_number_segments = 10
        bezier_mask = BezierMask(number_of_segments=number_segments,
                                 min_number_of_segments=min_number_segments)
        for i in range(100):
            bezier_mask.decrease_number_of_segments()

        expected_number_of_segments = min_number_segments
        actual_number_of_segments = bezier_mask.number_of_segments
        self.assertEqual(expected_number_of_segments, actual_number_of_segments, msg)


if __name__ == "__main__":
    main()
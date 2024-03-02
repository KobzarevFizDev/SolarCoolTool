from unittest import main, TestCase

from PyQt5.QtCore import QPoint

from Models.app_models import InterestingSolarRegion

class InterestingSolarRegionTest(TestCase):
    def test_align_to_square(self) -> None:
        msg1 = "Bottom left isnt correct"
        msg2 = "Top right isnt correct"
        integration_solar_region = InterestingSolarRegion()
        integration_solar_region.set_top_right(QPoint(100, 0))
        integration_solar_region.set_bottom_left(QPoint(0, 300))
        actual_top_right: QPoint = integration_solar_region.top_right
        actual_bottom_left: QPoint = integration_solar_region.bottom_left
        expected_top_right: QPoint = QPoint(150, 300)
        expected_bottom_left: QPoint = QPoint(-50, 100)
        self.assertEqual(expected_bottom_left, actual_bottom_left, msg1)
        self.assertEqual(expected_top_right, actual_top_right, msg2)


if __name__ == "__main__":
    main()

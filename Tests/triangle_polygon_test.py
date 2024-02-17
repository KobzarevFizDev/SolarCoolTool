from unittest import TestCase, main
from mask_exporter import TrianglePolygon

from PyQt5.QtCore import QPoint


class TrianglePolygonTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_bounding_box_case1(self) -> None:
        message1 = "tl of bounding box in case 1 - Wrong"
        message2 = "br of bounding box in case 1 - Wrong"
        a = QPoint(100, 100)
        b = QPoint(200, 200)
        c = QPoint(200, 100)
        polygon = TrianglePolygon(a, b, c)
        actualTopLeft, actualBottomRight = polygon.boundingBox
        print("actual = {0}".format(actualBottomRight))
        exceptTopLeft = QPoint(100, 200)
        exceptBottomRight = QPoint(200, 100)
        self.assertEqual(exceptTopLeft, actualTopLeft, message1)
        self.assertEqual(exceptBottomRight, actualBottomRight, message2)

    def tearDown(self) -> None:
        pass
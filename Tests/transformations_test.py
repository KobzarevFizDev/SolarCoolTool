from unittest import TestCase, main

from PyQt5.QtCore import QPoint

from transformations import transformPointFromViewToImage

class TransformationTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_point_transformation_case1(self) -> None:
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointOnView = QPoint(600, 600)
        zoom = 1
        exceptPointInImage = QPoint(4096, 4096)

        actualPointInImage = transformPointFromViewToImage(pointOnView, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(actualPointInImage,exceptPointInImage, "Point transformation case 1- wrong!")

    def test_point_transformation_case2(self) -> None:
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointOnView = QPoint(300, 300)
        zoom = 1
        exceptPointInImage = QPoint(2048, 2048)

        actualPointInImage = transformPointFromViewToImage(pointOnView, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(actualPointInImage,exceptPointInImage, "Point transformation case 2 - wrong!")

    def test_point_transformation_case3(self) -> None:
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointOfView = QPoint(600, 600)
        zoom = 2
        exceptPoint = QPoint(2048, 2048)

        actualPointInImage = transformPointFromViewToImage(pointOfView, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(actualPointInImage, exceptPoint, "Point transformation case 3 - wrong")

    def tearDown(self) -> None:
        pass

if __name__ == "__main__":
    main()
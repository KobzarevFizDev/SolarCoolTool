from unittest import TestCase, main

from PyQt5.QtCore import QPoint

from transformations import transformPointFromViewToImage, transformPointFromImageToView

class TransformationTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_point_transformation_from_view_to_image_case1(self) -> None:
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointOnView = QPoint(600, 600)
        zoom = 1
        exceptPointInImage = QPoint(4096, 4096)

        actualPointInImage = transformPointFromViewToImage(pointOnView, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(exceptPointInImage, actualPointInImage, "Point transformation case 1- wrong!")

    def test_point_transformation_from_view_to_image_case2(self) -> None:
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointOnView = QPoint(300, 300)
        zoom = 1
        exceptPointInImage = QPoint(2048, 2048)

        actualPointInImage = transformPointFromViewToImage(pointOnView, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(exceptPointInImage, actualPointInImage, "Point transformation case 2 - wrong!")

    def test_point_transformation_from_view_to_image_case3(self) -> None:
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointOfView = QPoint(600, 600)
        zoom = 2
        exceptPointInImage = QPoint(2048, 2048)

        actualPointInImage = transformPointFromViewToImage(pointOfView, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(exceptPointInImage, actualPointInImage, "Point transformation case 3 - wrong")

    def test_point_transformation_from_view_to_image_case4(self):
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointInView = QPoint(600, 600)
        zoom = 2
        offset = QPoint(-600, -600)
        exceptPointInImage = QPoint(4096, 4096)

        actualPointInImage = transformPointFromViewToImage(pointInView, sizeOfView, sizeOfImage, zoom, offset)
        self.assertEqual(exceptPointInImage, actualPointInImage, "Point transformation case 4- wrong!")

    def test_point_transformation_from_image_to_view_case1(self):
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointInImage = QPoint(4096, 4096)
        zoom = 1
        exceptPointInView = QPoint(600, 600)

        actualPointInView = transformPointFromImageToView(pointInImage, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(exceptPointInView, actualPointInView, "Point transformation case 1- wrong!")

    def test_point_transformation_from_image_to_view_case2(self):
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointInImage = QPoint(2048, 2048)
        zoom = 1
        exceptPointInView = QPoint(300, 300)

        actualPointInView = transformPointFromImageToView(pointInImage, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(exceptPointInView, actualPointInView, "Point transformation case 2- wrong!")

    def test_point_transformation_from_image_to_view_case3(self):
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointInImage = QPoint(2048, 2048)
        zoom = 2
        exceptPointInView = QPoint(600, 600)

        actualPointInView = transformPointFromImageToView(pointInImage, sizeOfView, sizeOfImage, zoom)
        self.assertEqual(exceptPointInView, actualPointInView, "Point transformation case 3- wrong!")


    def test_point_transformation_from_image_to_view_case4(self):
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointInImage = QPoint(2048, 2048)
        zoom = 2
        offset = QPoint(-600, -600)
        exceptPointInView = QPoint(0, 0)

        actualPointInView = transformPointFromImageToView(pointInImage, sizeOfView, sizeOfImage, zoom, offset)
        self.assertEqual(exceptPointInView, actualPointInView, "Point transformation case 4- wrong!")


    def test_point_transformation_from_image_to_view_case5(self):
        sizeOfView = (600, 600)
        sizeOfImage = (4096, 4096)
        pointInImage = QPoint(4096, 4096)
        zoom = 2
        offset = QPoint(-600, -600)
        exceptPointInView = QPoint(600, 600)

        actualPointInView = transformPointFromImageToView(pointInImage, sizeOfView, sizeOfImage, zoom, offset)
        self.assertEqual(exceptPointInView, actualPointInView, "Point transformation case 5- wrong!")


    def tearDown(self) -> None:
        pass

if __name__ == "__main__":
    main()
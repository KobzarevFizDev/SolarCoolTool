from unittest import main, TestCase

from PyQt5.QtCore import QPoint

from Models.models import ViewportTransform

class ViewportTransformTest(TestCase):
    def setUp(self) -> None:
        self.__viewport_transform = ViewportTransform()

    def test_transformation_from_view_to_image_case1(self) -> None:
        msg = "From view to image case 1 - fail"
        self.__viewport_transform.zoom = 1
        self.__viewport_transform.offset = QPoint(0, 0)
        point_in_view = QPoint(600, 600)
        expected_point_in_image = QPoint(4096, 4096)
        actual_point_in_image = (self.__viewport_transform
                                 .transform_from_viewport_pixel_to_image_pixel(point_in_view))
        self.assertEqual(expected_point_in_image, actual_point_in_image, msg)

    def test_transformation_from_view_to_image_case2(self) -> None:
        msg = "From view to image case 2 - fail"
        self.__viewport_transform.zoom = 1
        self.__viewport_transform.offset = QPoint(0, 0)
        point_in_view = QPoint(300, 300)
        expected_point_in_image = QPoint(2048, 2048)
        actual_point_in_image = (self.__viewport_transform
                                 .transform_from_viewport_pixel_to_image_pixel(point_in_view))
        self.assertEqual(expected_point_in_image, actual_point_in_image, msg)

    def test_transformation_from_view_to_image_case3(self) -> None:
        msg = "From view to image case 3 - fail"
        self.__viewport_transform.zoom = 2
        self.__viewport_transform.offset = QPoint(0, 0)
        point_in_view = QPoint(600, 600)
        expected_point_in_image = QPoint(2048, 2048)
        actual_point_in_image = (self.__viewport_transform
                                 .transform_from_viewport_pixel_to_image_pixel(point_in_view))
        self.assertEqual(expected_point_in_image, actual_point_in_image, msg)

    def test_transformation_from_view_to_image_case4(self) -> None:
        msg = "From view to image case 4 - fail"
        self.__viewport_transform.zoom = 2
        self.__viewport_transform.offset = QPoint(-600, -600)
        point_in_view = QPoint(600, 600)
        expected_point_in_image = QPoint(4096, 4096)
        actual_point_in_image = (self.__viewport_transform
                                 .transform_from_viewport_pixel_to_image_pixel(point_in_view))
        self.assertEqual(expected_point_in_image, actual_point_in_image, msg)

    def test_transformation_from_image_to_view_case1(self) -> None:
        msg = "From image to view case 1 - fail"
        self.__viewport_transform.zoom = 1
        point_in_image = QPoint(4096, 4096)
        expected_point_in_image = QPoint(600, 600)
        actual_point_in_image = (self.__viewport_transform
                                 .transform_from_image_pixel_to_viewport_pixel(point_in_image))
        self.assertEqual(expected_point_in_image, actual_point_in_image, msg)

    def test_transformation_from_image_to_view_case2(self) -> None:
        msg = "From image to view case 2 - fail"
        self.__viewport_transform.zoom = 1
        point_in_image = QPoint(2048, 2048)
        expected_point_in_image = QPoint(300, 300)
        actual_point_in_image = (self.__viewport_transform
                                 .transform_from_image_pixel_to_viewport_pixel(point_in_image))
        self.assertEqual(expected_point_in_image, actual_point_in_image, msg)

    def test_transformation_from_image_to_view_case3(self) -> None:
        msg = "From image to view case 3 - fail"
        self.__viewport_transform.zoom = 2
        point_in_image = QPoint(2048, 2048)
        expected_point_in_image = QPoint(600, 600)
        actual_point_in_image = (self.__viewport_transform
                                 .transform_from_image_pixel_to_viewport_pixel(point_in_image))
        self.assertEqual(expected_point_in_image, actual_point_in_image, msg)

    def test_transformation_from_image_to_view_case4(self) -> None:
        msg = "From image to view case 4 - fail"
        self.__viewport_transform.zoom = 2
        self.__viewport_transform.offset = QPoint(-600, -600)
        point_in_image = QPoint(2048, 2048)
        expected_point_in_image = QPoint(0, 0)
        actual_point_in_image = (self.__viewport_transform
                                 .transform_from_image_pixel_to_viewport_pixel(point_in_image))
        self.assertEqual(expected_point_in_image, actual_point_in_image, msg)


if __name__ == "__main__":
    main()

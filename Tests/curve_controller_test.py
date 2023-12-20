from unittest import TestCase, main

from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint

from Controllers.curve_editor_controller import CurveEditorController
from solar_tool_window import CurveEditorWindow
from Models.solar_editor_model import SolarEditorModel, CurveAreaSegment

from images_indexer import ImagesIndexer

class CurveControllerTest(TestCase):
    def setUp(self) -> None:
        self.app = QtWidgets.QApplication([])
        mainAppWindow = CurveEditorWindow()
        model = SolarEditorModel(ImagesIndexer("C:\\SolarImages"))
        self.controller = CurveEditorController(model, mainAppWindow)

    def test_calculate_tops_points_forming_area(self):
        pointsFormingBroken = [QPoint(100, 100),
                               QPoint(120, 105),
                               QPoint(140, 99),
                               QPoint(150, 106),
                               QPoint(160, 80)]

        expectedPoints = [QPoint(100, 110),
                          QPoint(120, 115),
                          QPoint(140, 109),
                          QPoint(150, 116),
                          QPoint(160, 90)]


        topPoints = self.controller.calculateTopPointsFormingArea(pointsFormingBroken, 20)
        self.assertEqual(topPoints, expectedPoints, "top points incorrect")

    def test_calculate_bottom_points_forming_area(self):
        pointsFormingBroken = [QPoint(100, 100),
                               QPoint(120, 105),
                               QPoint(140, 99),
                               QPoint(150, 106),
                               QPoint(160, 80)]

        expectedPoints = [QPoint(100, 90),
                          QPoint(120, 95),
                          QPoint(140, 89),
                          QPoint(150, 96),
                          QPoint(160, 70)]

        bottomPoints = self.controller.calculateBottomPointsFormingArea(pointsFormingBroken, 20)
        self.assertEqual(bottomPoints, expectedPoints, "bottom points incorrect")

    def test_calculate_area_segments(self):
        pointsFormingBroken = [QPoint(100, 100),
                               QPoint(120, 105),
                               QPoint(140, 99)]

        topPoints = self.controller.calculateTopPointsFormingArea(pointsFormingBroken, 20)
        bottomPoints = self.controller.calculateBottomPointsFormingArea(pointsFormingBroken, 20)
        calculatedSegments = self.controller.calculateAreaSegments(topPoints, bottomPoints)

        expectedSegment1 = CurveAreaSegment(QPoint(120, 115),
                               QPoint(100, 110),
                               QPoint(120, 95),
                               QPoint(100, 90))

        expectedSegment2 = CurveAreaSegment(QPoint(140, 109),
                               QPoint(120, 115),
                               QPoint(140, 89),
                               QPoint(120, 95))

        calculatedSegment1 = calculatedSegments[0]
        calculatedSegment2 = calculatedSegments[1]

        self.assertEqual(expectedSegment1, calculatedSegment1, "segment 1 is incorrect")
        self.assertEqual(expectedSegment2, calculatedSegment2, "segment 2 is incorrect")

if __name__ == "__main__":
    main()


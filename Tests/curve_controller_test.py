from unittest import TestCase, main

from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint

from Controllers.curveEditorController import CurveEditorController
from Models.curveAreaModel import CurveAreaModel
from SolarToolWindow import CurveEditorWindow


class CurveControllerTest(TestCase):
    def setUp(self) -> None:
        self.app = QtWidgets.QApplication([])
        mainAppWindow = CurveEditorWindow()
        model = CurveAreaModel()
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


        topPoints = self.controller.calculateTopsPointsFormingArea(pointsFormingBroken, 20)

        self.assertEqual(topPoints, expectedPoints, "top points incorrect")

if __name__ == "__main__":
    main()

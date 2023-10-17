from unittest import TestCase, main

from PyQt5 import QtWidgets

import functions_for_tests

from PyQt5.QtCore import QPoint

from Controllers.curveEditorController import CurveEditorController
from Models.curveAreaModel import CurveAreaModel
from SolarToolWindow import CurveEditorWindow


class ExampleTest(TestCase):
    def test_summ(self):
        self.assertEqual(functions_for_tests.summ(3, 4), 7)

    def test_diff(self):
        self.assertEqual(functions_for_tests.diff(4,2), 2)

    def test_array(self):
        self.assertEqual([1,2,3,4], [1,2,3,4])

if __name__ == "__main__":
    main(exit=False)
import unittest
from PyQt5 import QtWidgets
from p3 import MyWidget


class TestMyWidget(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.widget = MyWidget()

    def test_some_feature(self):
        # Test that some feature of the widget is working as expected
        self.assertEqual(self.widget.some_feature(), 42)


if __name__ == '__main__':
    unittest.main()
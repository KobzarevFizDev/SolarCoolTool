from typing import Union
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage
from TimeDistancePlotBuilder.transformations import *


def case1():
    p_1 = QPoint(100, 100)
    z_2 = QPoint(300, 300)
    print('p*({0},{1}) -> p**(?,?)'.format(p_1.x(), p_1.y()))
    transform_point_from_bezier_mask_to_solar_view()

def main():
    print('transformations tests')
    case1()


if __name__ == '__main__':
    main()
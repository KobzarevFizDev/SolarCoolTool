import math
from typing import List

from PyQt5.QtCore import QPoint
import numpy as np
import numpy.typing as npt

def main():
    raster = create_raster(20)
    DDACicle(raster, 5,5,3)
    show_raster(raster, 10)

def create_raster(size):
    raster = ['[ ]'] * size # создает одномерный массив длинной size
    for i in range(size):
        raster[i] = ['[ ]'] * size
    return raster

def show_raster(raster, size):
    for x in range(size):
        line = ""
        for y in range(size):
            line += str(raster[x][y])
        print(line)

def get_pixels_of_line(x1, y1, x2, y2, L: int = None) -> List[QPoint]:
    if L == None:
        L = max(abs(round(x1) - round(x2)), abs(round(y1) - round(y2)))
    delta_x = (x2 - x1)/L
    delta_y = (y2 - y1)/L
    x = x1
    y = y1
    rasterOfLine: List[QPoint] = list()

    while L > 0:
        x += delta_x
        y += delta_y
        rasterOfLine.append(QPoint(round(x), round(y)))
        L -= 1
    return rasterOfLine


def get_pixels_of_cicle(x_c: int, y_c: int, r: int) -> List[QPoint]:
    pixels = list()
    top_right_border_point_x = int(math.ceil(x_c + r/2))
    top_right_border_point_y = int(math.ceil(y_c + r/2))

    bottom_left_border_point_x = int(math.floor(x_c - r/2))
    bottom_left_border_point_y = int(math.floor(y_c - r/2))


    for x in range(bottom_left_border_point_x - 3, top_right_border_point_x + 3):
        for y in range(bottom_left_border_point_y - 3, top_right_border_point_y + 3):
            delta_x = x_c - x
            delta_y = y_c - y
            delta = math.sqrt(delta_x**2 + delta_y** 2)
            if delta <= r:
                pixels.append(QPoint(x, y))

    return pixels

def DDACicle(raster, x_c:int, y_c: int, r: int):
    top_right_border_point_x = int(math.ceil(x_c + r/2))
    top_right_border_point_y = int(math.ceil(y_c + r/2))

    bottom_left_border_point_x = int(math.floor(x_c - r/2))
    bottom_left_border_point_y = int(math.floor(y_c - r/2))

    set_pixel_in_raster(raster, top_right_border_point_x, top_right_border_point_y, '[*]')
    set_pixel_in_raster(raster, bottom_left_border_point_x, bottom_left_border_point_y, '[*]')
    set_pixel_in_raster(raster, x_c, y_c, '[+]')


    for x in range(bottom_left_border_point_x - 3, top_right_border_point_x + 3):
        for y in range(bottom_left_border_point_y - 3, top_right_border_point_y + 3):
            delta_x = x_c - x
            delta_y = y_c - y
            delta = math.sqrt(delta_x**2 + delta_y** 2)
            print(delta)
            if delta <= r:
                set_pixel_in_raster(raster, x, y, '[+]')


def DDALine(raster, x1, y1, x2, y2):
    L = max(abs(round(x1) - round(x2)), abs(round(y1) - round(y2)))
    delta_x = (x2 - x1)/L
    delta_y = (y2 - y1)/L

    x = x1
    y = y1

    while L > 0:
        x += delta_x
        y += delta_y
        set_pixel_in_raster(raster, round(x), round(y), '[*]')
        L -= 1


def set_pixel_in_raster(raster, x, y, symbol):
    print("set {0} {1}".format(x, y))
    raster[x][y] = symbol

if __name__ == "__main__":
    main()
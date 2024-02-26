import math
from typing import List

from PyQt5.QtCore import QPoint


def main():
    raster = createRaster(10)
    DDALine(raster, 1, 1, 9, 9)
    showRaster(raster, 10)

def createRaster(size):
    raster = ['[ ]'] * size # создает одномерный массив длинной size
    for i in range(size):
        raster[i] = ['[ ]'] * size
    return raster

def showRaster(raster, size):
    for x in range(size):
        line = ""
        for y in range(size):
            line += str(raster[x][y])
        print(line)

def getRasterOfLine(x1, y1, x2, y2) -> List[QPoint]:
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


def DDALine(raster, x1, y1, x2, y2):
    L = max(abs(round(x1) - round(x2)), abs(round(y1) - round(y2)))
    delta_x = (x2 - x1)/L
    delta_y = (y2 - y1)/L

    x = x1
    y = y1

    while L > 0:
        x += delta_x
        y += delta_y
        setPixelInRaster(raster, round(x), round(y), '[*]')
        L -= 1


def setPixelInRaster(raster, x, y, symbol):
    print("set {0} {1}".format(x, y))
    raster[x][y] = symbol

if __name__ == "__main__":
    main()
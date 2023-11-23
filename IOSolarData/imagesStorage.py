import os

import sunpy.visualization.colormaps.cm

import numpy as np
from PyQt5.QtGui import QImage, QColor
from astropy.io import fits

class ImagesStorage:
    def __init__(self):
        self.path_of_files_in_storage = list(filter((lambda f : "image" in f), os.listdir("Images")))

    def read_test_image(self, w, h):
        print(sunpy.visualization.colormaps.cm.sdoaia171(1))
        data = np.ones((w, h, 3), dtype=np.uint8)
        for x in range(w):
            for y in range(h):
                data[x][y][0] = 254
                data[x][y][1] = 150
                data[x][y][2] = 1
        return QImage(data, data.shape[1], data.shape[0], 3*w, QImage.Format_RGB888)

    def read_image_by_index(self, index:int):
        path = self.path_of_files_in_storage[index]
        readed_data = fits.open("Images/" + path)[1].data
        img_w = readed_data.shape[0]
        img_h = readed_data.shape[1]
        cm = sunpy.visualization.colormaps.cm.sdoaia193
        a = np.array(255 * cm(readed_data), dtype=np.uint8)
        return QImage(a, img_h, img_w, 4 * img_w, QImage.Format_RGBA8888)

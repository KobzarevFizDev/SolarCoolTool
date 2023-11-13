import os

from PyQt5.QtGui import QImage
from astropy.io import fits


class ImagesStorage:
    def __init__(self):
        self.path_of_files_in_storage = list(filter((lambda f : "image" in f), os.listdir("Images")))


    def read_image_by_index(self, index:int):
        path = self.path_of_files_in_storage[index]
        data = fits.open("Images/" + path)[1].data
        return QImage(data, data.shape[1], data.shape[0], QImage.Format_Indexed8)
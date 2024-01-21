from typing import TYPE_CHECKING
from PIL import Image
import numpy as np


class MaskExporter:
    def __init__(self, solarEditorModel):
        self.__solarEditorModel = solarEditorModel

    def exportToBmp(self, pathToExport):
        data = 255 * np.ones((10,10), dtype=np.uint8)
        image = Image.fromarray(data, "L")
        image.save(pathToExport)
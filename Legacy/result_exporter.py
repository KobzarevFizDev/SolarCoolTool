from dda import get_pixels_of_line
from typing import TYPE_CHECKING, List
from PyQt5.QtCore import QPoint

if TYPE_CHECKING:
    from Legacy.solar_editor_model import SolarEditorModel

class ResultExporter:
    def __init__(self, solarEditorModel):
        self.__solarEditorModel: SolarEditorModel = solarEditorModel

    def exportResult(self):
        slices: List[List[QPoint]] = self.__rasterizeMaskToSlices()
        self.__createResult2dArray(slices)

    def __rasterizeMaskToSlices(self) -> List[List[QPoint]]:
        widthOfMask = 30
        rastersOfSlices = list()
        for i in range(widthOfMask):
            points: List[QPoint] = self.__solarEditorModel.maskSpline.getSliceOfMaskSpline(i)
            rasterOfSlice: List[QPoint] = self.__rasterizeSlice(points)
            rastersOfSlices.append(rasterOfSlice)
        return rastersOfSlices

    def __rasterizeSlice(self, points) -> List[QPoint]:
        L = len(points)
        raster: List[QPoint] = list()
        for i in range(L - 1):
            p1: QPoint = points[i]
            p2: QPoint = points[i+1]

            p1x = int(p1.x())
            p1y = int(p1.y())
            p2x = int(p2.x())
            p2y = int(p2.y())

            raster += get_pixels_of_line(p1x, p1y, p2x, p2y)
        return raster

    def __createResult2dArray(self, slices: List[List[QPoint]]):
        numberOfPixelsInLongestSlice = self.__getNumberOfPixelInLongestSlice(slices)

        result = [0] * len(slices)

        numberOfSlices = len(slices)
        for i in range(numberOfSlices):
            currentSlice = slices[i]
            numberOfPixelsInCurrentSlice = len(currentSlice)
            numberOfPixelNeedToCreate = numberOfPixelsInLongestSlice - numberOfPixelsInCurrentSlice
            result[i] = self.__getPixelsOfSlice(slices, i, numberOfPixelNeedToCreate)
            print(result[i])
            print("Longest = {0}. Current = {1} Need to create = {2}"
                  .format(numberOfPixelsInLongestSlice, numberOfPixelsInCurrentSlice, numberOfPixelNeedToCreate))

    def __getPixelsOfSlice(self,
                           slices: List[List[QPoint]],
                           currentSliceIndex:int,
                           numberOfPixelsNeedToCreate:int) -> List[int]:
        pixelsValueInSlice = list()
        step = 10 # todo: Придумать иначе
        slice = slices[currentSliceIndex]
        numberOfPixelsNeedToCreateAtMoment = numberOfPixelsNeedToCreate
        i = 0
        while i < len(slice) + numberOfPixelsNeedToCreateAtMoment:
            i += 1
            pixelValue = self.__solarEditorModel.currentSolarImageAsFITS[currentSliceIndex][i]
            pixelsValueInSlice.append(pixelValue)
            if i % step == 0:
                numberOfPixelsNeedToCreateAtMoment -= 1
                a = self.__solarEditorModel.currentSolarImageAsFITS[currentSliceIndex][i-1]
                b = self.__solarEditorModel.currentSolarImageAsFITS[currentSliceIndex][i+1]
                pixelsValueInSlice.append(int((a+b)/2)) # todo: интерполировать значения
        print(len(pixelsValueInSlice))
        return pixelsValueInSlice


    def __getNumberOfPixelInLongestSlice(self, slices):
        numberOfPixels = 0
        for slice in slices:
            if len(slice) > numberOfPixels:
                numberOfPixels = len(slice)
        return numberOfPixels

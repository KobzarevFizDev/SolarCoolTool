import numpy.typing as npt

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import Colormap

from TimeDistancePlotBuilder.Models.app_models import SolarRenderPlot

class TDP_MatplotlibPreviewWidget(FigureCanvas):
    def __init__(self,
                 tdp_rgb_array: npt.NDArray,
                 channel: int,
                 parent=None):
        self.__tdp_rgb_array: npt.NDArray = tdp_rgb_array
        self.__channel: int = channel

        self.__fig: Figure = self.__create_figure_by_tdp()
        self.__axes = self.__fig.add_subplot()
        super().__init__(self.__fig)

        self.show_time_distance_plot()

    def change_tdp(self, tdp_rgb_array: npt.NDArray) -> None:
        self.__tdp_rgb_array = tdp_rgb_array
        self.update_plot()

    def change_channel(self, new_channel: int) -> None:
        self.__channel = new_channel
        self.update_plot()

    def show_time_distance_plot(self) -> None:
        self.__axes.set_xlabel("Время, С")
        self.__axes.set_ylabel("Дистанция вдоль петли, Mm")
        self.__axes.set_title(f"Канал {self.__channel} A")
        self.__axes.imshow(self.__tdp_rgb_array)

    def __create_figure_by_tdp(self) -> Figure:
        dpi = 100
        height_in_pixels: int = self.__tdp_rgb_array.shape[0]
        width_in_pixels: int = self.__tdp_rgb_array.shape[1]
        fig = Figure(figsize=(width_in_pixels / dpi, height_in_pixels / dpi), dpi=dpi)
        return fig

    def update_plot(self) -> None:
        self.__axes.clear() 
        self.show_time_distance_plot()
        self.draw() 


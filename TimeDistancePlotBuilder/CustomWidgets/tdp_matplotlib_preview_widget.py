import numpy.typing as npt

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import Colormap

class TDP_MatplotlibPreviewWidget(FigureCanvas):
    def __init__(self,
                 time_distance_plot: npt.NDArray,
                 channel: int,
                 cmap: Colormap,
                 parent=None):
        self.__tdp: npt.NDArray = time_distance_plot
        self.__channel: int = channel
        self.__cmap: Colormap = cmap

        self.__fig: Figure = self.__create_figure_by_tdp()
        self.__axes = self.__fig.add_subplot()
        super().__init__(self.__fig)

        self.show_time_distance_plot()

    def change_tdp(self, new_tdp: npt.NDArray) -> None:
        self.__tdp = new_tdp
        self.update_plot()

    def change_channel(self, new_channel: int, new_cmap: Colormap) -> None:
        self.__channel = new_channel
        self.__cmap = new_cmap
        self.update_plot()

    def show_time_distance_plot(self) -> None:
        self.__axes.set_xlabel("Время, С")
        self.__axes.set_ylabel("Дистанция вдоль петли, Mm")
        self.__axes.set_title(f"Канал {self.__channel} A")
        self.__axes.imshow(self.__tdp, cmap=self.__cmap)

    def __create_figure_by_tdp(self) -> Figure:
        dpi = 100
        height_in_pixels: int = self.__tdp.shape[0]
        width_in_pixels: int = self.__tdp.shape[1]
        fig = Figure(figsize=(width_in_pixels / dpi, height_in_pixels / dpi), dpi=dpi)
        return fig

    def update_plot(self) -> None:
        self.__axes.clear() 
        self.show_time_distance_plot()
        self.draw() 


from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsScene, QGraphicsView, QGraphicsProxyWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from TimeDistancePlotBuilder.Models.app_models import AppModel, ZoneInteresting
from TimeDistancePlotBuilder.CustomWidgets.zone_interesting_control_point_widget import ZoneInterestingPositionControlPointWidget, ZoneInterestingSizeControlPointWidget
from TimeDistancePlotBuilder.CustomWidgets.plot_widget import PlotWidget

class SolarViewerWidget(QWidget):
    zoom_image_signal = pyqtSignal(int, int)
    move_image_signal = pyqtSignal(int, int)
    on_changed_position_of_zone_interesting_position_anchor_signal = pyqtSignal(int ,int)
    on_changed_position_of_zone_interesting_size_anchor = pyqtSignal(int, int)

    def __init__(self, solar_viewer_controller, app_model: AppModel):
        super(SolarViewerWidget, self).__init__()
        self.__zone_interesting_model: ZoneInteresting = app_model.zone_interesting
        self.__app_model: AppModel = app_model
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setMouseTracking(True)
        self.__scene = QGraphicsScene(self)
        self.__scene.setSceneRect(0, 0, 600, 600)
        self.__view = QGraphicsView(self.__scene, self)
        self.__view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view_rect = self.contentsRect()
        self.__view.setSceneRect(0, 0, view_rect.width(), view_rect.height())
        self.__view.show()
        
        self.__pixmap: QPixmap = QPixmap(600, 600)
        self.__offset: QPoint = QPoint(0, 0)

        self.__solar_plot: PlotWidget = None

        self.__zone_interesting_position_anchor: ZoneInterestingPositionControlPointWidget = None

        self.__create_solar_plot()
        self.__manipulator_zone_interesting_position_anchor = self.__create_zone_interesting_position_anchor()


    def __create_solar_plot(self) -> QGraphicsProxyWidget:
        self.__pixmap.fill(Qt.green)
        self.__solar_plot = PlotWidget(self.__pixmap, self.__offset)
        self.__solar_plot.zoom_image_signal.connect(self.__on_zoom_image)
        self.__solar_plot.move_image_signal.connect(self.__on_move_image)
        proxy = self.__scene.addWidget(self.__solar_plot)
        return proxy
    

    def __create_zone_interesting_position_anchor(self) -> QGraphicsProxyWidget:
        self.__zone_interesting_position_anchor = ZoneInterestingPositionControlPointWidget(self.__app_model)
        self.__zone_interesting_position_anchor.change_position_signal.connect(self.__on_changed_position_of_zone_interesting_position_anchor)
        proxy = self.__scene.addWidget(self.__zone_interesting_position_anchor)
        return proxy


    def update_widget(self):
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.__draw_solar_frame()
        self.__draw_border_of_zone_interesting()    

    def set_solar_frame_to_draw(self, pixmap: QPixmap, offset: QPoint) -> None:
        self.__pixmap = pixmap
        self.__offset = offset

    def __draw_solar_frame(self) -> None:
        self.__solar_plot.update_plot(self.__pixmap, self.__offset)

    def __draw_border_of_zone_interesting(self) -> None:
        painter = QPainter()
        painter.begin(self)

        borderPen = QPen(Qt.red, 2.0, Qt.DotLine)
        diagonalPen = QPen(Qt.blue, 3.0, Qt.DotLine)
        painter.setPen(borderPen)
        
        tr: QPoint = self.__zone_interesting_model.top_right_in_view
        tl: QPoint = self.__zone_interesting_model.top_left_in_view
        br: QPoint = self.__zone_interesting_model.bottom_right_in_view
        bl: QPoint = self.__zone_interesting_model.bottom_left_in_view

        painter.drawLine(tl, tr)
        painter.drawLine(tr, br)
        painter.drawLine(br, bl)
        painter.drawLine(bl, tl)

        painter.setPen(diagonalPen)
        painter.drawLine(br, tl)

        painter.end()

    def __on_move_image(self, pos_x: int, pos_y: int) -> None:
        self.move_image_signal.emit(pos_x, pos_y)

    def __on_zoom_image(self, zoom, tmp) -> None:
        self.zoom_image_signal.emit(zoom, tmp)

    def __on_changed_position_of_zone_interesting_position_anchor(self, pos_x: int, pos_y: int) -> None:
        self.on_changed_position_of_zone_interesting_position_anchor_signal.emit(pos_x, pos_y)

    def __on_changed_position_of_zone_interesting_position_anchor(self, pos_x: int, pos_y: int) -> None:
        self.on_changed_position_of_zone_interesting_size_anchor.emit(pos_x, pos_y)
        
        #new_pos = QPoint(pos_x, pos_y)
        #self.__zone_interesting_model.set_position_of_position_anchor(new_pos)
        #self.__app_model.notify_observers()
    
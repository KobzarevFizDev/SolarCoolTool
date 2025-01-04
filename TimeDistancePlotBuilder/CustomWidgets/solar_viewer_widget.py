from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsScene, QGraphicsView, QGraphicsProxyWidget, QPushButton
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QPointF
from TimeDistancePlotBuilder.Models.app_models import AppModel, ZoneInteresting
from TimeDistancePlotBuilder.CustomWidgets.zone_interesting_control_point_widget import ZoneInterestingPositionControlPointWidget, ZoneInterestingSizeControlPointWidget
from TimeDistancePlotBuilder.CustomWidgets.plot_widget import PlotWidget

class SolarViewerWidget(QWidget):
    zoom_image_signal = pyqtSignal(int, int)
    move_image_signal = pyqtSignal(int, int)
    on_changed_position_of_zone_interesting_position_anchor_signal = pyqtSignal(int ,int)
    on_changed_position_of_zone_interesting_size_anchor_signal = pyqtSignal(int, int)
    export_signal = pyqtSignal(QWidget)

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
        self.__proxy_zone_interesting_position_anchor: QGraphicsProxyWidget = self.__create_zone_interesting_position_anchor()
        self.__proxy_zone_interesting_size_anchor: QGraphicsScene = self.__create_zone_interesting_size_anchor()

        self.__temps_objects_on_scene = []

        self.__export_button: QPushButton = self.__create_export_button()

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
    
    def __create_zone_interesting_size_anchor(self) -> QGraphicsProxyWidget:
        self.__zone_interesting_size_anchor = ZoneInterestingSizeControlPointWidget(self.__app_model)
        self.__zone_interesting_size_anchor.change_position_signal.connect(self.__on_changed_position_of_zone_interesting_size_anchor)
        proxy = self.__scene.addWidget(self.__zone_interesting_size_anchor)
        return proxy
    
    def __create_export_button(self) -> QPushButton:
        export_button = QPushButton("Export", self)
        export_button.clicked.connect(self.__on_export_button_clicked)
        return export_button
    
    def __on_export_button_clicked(self) -> None:
        self.export_signal.emit(self)

    def update_widget(self):
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.__clear_temps_objects()
        self.__draw_solar_frame()
        self.__draw_border_of_zone_interesting() 

    def update_position_of_zone_interesting_position_anchor(self, pos: QPoint) -> None:
        self.__zone_interesting_position_anchor.set_pos(pos)

    def update_position_of_zone_interesting_size_anchor(self, pos: QPoint) -> None:
        self.__zone_interesting_size_anchor.set_pos(pos)

    def set_solar_frame_to_draw(self, pixmap: QPixmap, offset: QPoint) -> None:
        self.__pixmap = pixmap
        self.__offset = offset

    def show_export_button(self) -> None:
        self.__export_button.show()

    def hide_export_button(self) -> None:
        self.__export_button.hide()

    def __draw_solar_frame(self) -> None:
        self.__solar_plot.update_plot(self.__pixmap, self.__offset)

    def __draw_border_of_zone_interesting(self) -> None:
        self.__draw_borders_lines()

    def __draw_borders_lines(self) -> None:
        pen = QPen(Qt.red, 3.0, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
        
        br = self.__zone_interesting_model.bottom_right_in_view
        tr = self.__zone_interesting_model.top_right_in_view
        bl = self.__zone_interesting_model.bottom_left_in_view
        tl = self.__zone_interesting_model.top_left_in_view
        
        br2tr_line = self.__scene.addLine(br.x(), br.y(), tr.x(), tr.y(), pen)
        tr2tl_line = self.__scene.addLine(tr.x(), tr.y(), tl.x(), tl.y(), pen)
        tl2bl_line = self.__scene.addLine(tl.x(), tl.y(), bl.x(), bl.y(), pen)
        bl2br_line = self.__scene.addLine(bl.x(), bl.y(), br.x(), br.y(), pen)

        self.__temps_objects_on_scene.append(br2tr_line)
        self.__temps_objects_on_scene.append(tr2tl_line)
        self.__temps_objects_on_scene.append(tl2bl_line)
        self.__temps_objects_on_scene.append(bl2br_line)


    def __clear_temps_objects(self) -> None:
        for item in self.__temps_objects_on_scene:
            self.__scene.removeItem(item)

        self.__temps_objects_on_scene.clear()

    def __on_move_image(self, pos_x: int, pos_y: int) -> None:
        self.move_image_signal.emit(pos_x, pos_y)

    def __on_zoom_image(self, zoom, tmp) -> None:
        self.zoom_image_signal.emit(zoom, tmp)

    def __on_changed_position_of_zone_interesting_position_anchor(self, pos_x: int, pos_y: int) -> None:
        relative_pos: QPointF = self.__proxy_zone_interesting_position_anchor.mapToScene(pos_x, pos_y)
        relative_pos_x: int = int(relative_pos.x())
        relative_pos_y: int = int(relative_pos.y())
        self.on_changed_position_of_zone_interesting_position_anchor_signal.emit(relative_pos_x, relative_pos_y)

    def __on_changed_position_of_zone_interesting_size_anchor(self, pos_x: int, pos_y: int) -> None:
        relative_pos: QPointF = self.__proxy_zone_interesting_size_anchor.mapToScene(pos_x, pos_y)
        relative_pos_x: int = int(relative_pos.x())
        relative_pos_y: int = int(relative_pos.y())
        self.on_changed_position_of_zone_interesting_size_anchor_signal.emit(relative_pos_x, relative_pos_y)

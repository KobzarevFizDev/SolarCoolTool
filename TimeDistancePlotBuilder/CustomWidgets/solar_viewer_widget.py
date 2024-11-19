from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from TimeDistancePlotBuilder.Models.app_models import AppModel, ZoneInteresting
from TimeDistancePlotBuilder.CustomWidgets.zone_interesting_control_point_widget import ZoneInterestingPositionControlPointWidget, ZoneInterestingSizeControlPointWidget

class SolarViewerWidget(QWidget):
    wheelScrollSignal = pyqtSignal(int, int)
    mouseMoveSignal = pyqtSignal(int, int)
    def __init__(self, solar_viewer_controller, app_model: AppModel):
        self.__zone_interesting_model: ZoneInteresting = app_model.zone_interesting
        self.__controller = solar_viewer_controller
        super(SolarViewerWidget, self).__init__()
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.red))
        self.setPalette(palette)
        self.label = QLabel(self)

        self.__pixmap: QPixmap = QPixmap()
        self.__offset: QPoint = QPoint(0, 0)
        self.__is_moved: bool = False



        self.__position_anchor_widget: ZoneInterestingPositionControlPointWidget = ZoneInterestingPositionControlPointWidget(self.__zone_interesting_model.top_right_in_view, app_model)
        self.__size_anchor_widget: ZoneInterestingSizeControlPointWidget = ZoneInterestingSizeControlPointWidget(self.__zone_interesting_model.bottom_left_in_view, app_model)


    def update_widget(self):
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        self.__draw_solar_frame(painter)
        self.__draw_border_of_zone_interesting(painter)
        painter.end()    


    def set_solar_frame_to_draw(self, pixmap: QPixmap, offset: QPoint) -> None:
        self.__pixmap = pixmap
        self.__offset = offset


    def __draw_solar_frame(self, painter: QPainter) -> None:
        painter.drawPixmap(self.__offset, self.__pixmap)


    def __draw_border_of_zone_interesting(self, painter: QPainter) -> None:
        
        #painter.setPen(QPen(Qt.red, 5.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

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


    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_moved = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_moved = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        current_x = event.x()
        current_y = event.y()
        if self.__is_moved:
            delta_x = current_x - self.__previous_x
            delta_y = current_y - self.__previous_y
            self.mouseMoveSignal.emit(delta_x, delta_y)
        self.__previous_x = current_x
        self.__previous_y = current_y

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.wheelScrollSignal.emit(event.angleDelta().x(), event.angleDelta().y())

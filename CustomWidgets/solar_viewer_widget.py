from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint


class SolarViewerWidget(QWidget):
    wheelScrollSignal = pyqtSignal(int, int)
    mouseMoveSignal = pyqtSignal(int, int)
    plotWasAllocatedSignal = pyqtSignal(QPoint, QPoint)
    def __init__(self, parent):
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
        self.__top_right_of_interesting_area: QPoint = QPoint(-1, -1)
        self.__bottom_left_of_interesting_area = QPoint(-1, -1)
        self.__top_right_of_interesting_area_was_selected: bool = False
        self.__is_moved: bool = False

        self.__previous_x: int = -1
        self.__previous_y: int = -1

    def set_solar_frame_to_draw(self, pixmap: QPixmap, offset: QPoint) -> None:
        self.__pixmap = pixmap
        self.__offset = offset

    def set_selected_zone_interesting(self, top_left: QPoint, bottom_right: QPoint) -> None:
        self.__top_right_of_interesting_area = top_left
        self.__bottom_left_of_interesting_area = bottom_right

    def update_widget(self):
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        self.__draw_solar_frame(painter)
        self.__draw_border_of_zone_interesting(painter)
        painter.end()


    def __draw_solar_frame(self, painter: QPainter) -> None:
        painter.drawPixmap(self.__offset, self.__pixmap)

    def __draw_border_of_zone_interesting(self, painter: QPainter) -> None:
        painter.setPen(QPen(Qt.red, 5.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        tl = self.__top_right_of_interesting_area
        br = self.__bottom_left_of_interesting_area

        if tl.x() == -1 or br.x() == -1:
            return

        p1 = QPoint(tl.x(), tl.y())
        p2 = QPoint(tl.x(), br.y())
        p3 = QPoint(br.x(), br.y())
        p4 = QPoint(br.x(), tl.y())

        painter.drawLine(p1, p2)
        painter.drawLine(p2, p3)
        painter.drawLine(p3, p4)
        painter.drawLine(p4, p1)

    # TODO: Пользователь может выбрать точки не в том порядке, модель должна уметь с этим работать
    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        if not self.__top_right_of_interesting_area_was_selected:
            self.__top_right_of_interesting_area = QPoint(a0.x(), a0.y())
            self.__top_right_of_interesting_area_was_selected = True
        else:
            self.__bottom_left_of_interesting_area = QPoint(a0.x(), a0.y())
            self.__top_right_of_interesting_area_was_selected = False
            self.plotWasAllocatedSignal.emit(self.__top_right_of_interesting_area, self.__bottom_left_of_interesting_area)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_moved = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.__is_moved = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        current_x = event.x()
        current_y = event.y()
        if self.__is_moved and not self.__previous_x == -1 and not self.__previous_y == -1:
            delta_x = current_x - self.__previous_x
            delta_y = current_y - self.__previous_y
            self.mouseMoveSignal.emit(delta_x, delta_y)
        self.__previous_x = current_x
        self.__previous_y = current_y

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.wheelScrollSignal.emit(event.angleDelta().x(), event.angleDelta().y())


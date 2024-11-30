from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from TimeDistancePlotBuilder.Models.app_models import AppModel, ZoneInteresting


class BaseZoneInterestingControlPointWidget(QWidget):
    change_position_signal = pyqtSignal(int, int)

    def __init__(self, app_model: AppModel):
        super().__init__()
        self.setFixedSize(20, 20)
        self._app_model: AppModel = app_model
        self._zone_interesting_model: ZoneInteresting = app_model.zone_interesting
        self._is_selected: bool = False
    
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self._is_selected = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self._is_selected = False

    def mouseMoveEvent(self, event) -> None:
        if self._is_selected == False:
            return
        
        self.change_position_signal.emit(event.x(), event.y())
        


class ZoneInterestingPositionControlPointWidget(BaseZoneInterestingControlPointWidget):
    def __init__(self, app_model):
        super().__init__(app_model)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.black, 2.0, Qt.DotLine))

        a: QPoint = QPoint(10, 20)
        b: QPoint = QPoint(10, 0)
        c: QPoint = QPoint(20, 10)
        d: QPoint = QPoint(0, 10)

        painter.drawLine(a, b)
        painter.drawLine(c, d)
        painter.end()
        super().paintEvent(event)


class ZoneInterestingSizeControlPointWidget(BaseZoneInterestingControlPointWidget):
    def __init__(self, point_model: QPoint, app_model):
        super().__init__(point_model, app_model)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter()
        painter.begin()
        painter.setPen(QPen(Qt.green, 2.0, Qt.DotLine))

        pos_x: int = self.__point_model.x()
        pos_y: int = self.__point_model.y() 

        a: QPoint = QPoint(pos_x, pos_y + 10)
        b: QPoint = QPoint(pos_x, pos_y - 10)
        c: QPoint = QPoint(pos_x - 10, pos_y)
        d: QPoint = QPoint(pos_x + 10, pos_y)

        painter.drawLine(a, b)
        painter.drawLine(c, d)
        painter.end()

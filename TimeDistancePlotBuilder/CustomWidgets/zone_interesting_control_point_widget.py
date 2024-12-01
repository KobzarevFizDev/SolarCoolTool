from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from TimeDistancePlotBuilder.Models.app_models import AppModel, ZoneInteresting


class BaseZoneInterestingControlPointWidget(QWidget):
    change_position_signal = pyqtSignal(int, int)

    def __init__(self, app_model: AppModel):
        super().__init__()
        self._size = 20
        self.setFixedSize(self._size, self._size)
        self._app_model: AppModel = app_model
        self._zone_interesting_model: ZoneInteresting = app_model.zone_interesting
        self._is_selected: bool = False

    def set_pos(self, new_pos: QPoint) -> None:
        pos_x: int = new_pos.x() - self._size // 2
        pos_y: int = new_pos.y() - self._size // 2

        self.move(QPoint(pos_x, pos_y))
    
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
        painter = QPainter(self)
        painter.setBrush(Qt.green)
        painter.drawRect(0, 0, self._size, self._size)


class ZoneInterestingSizeControlPointWidget(BaseZoneInterestingControlPointWidget):
    def __init__(self, app_model):
        super().__init__(app_model)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setBrush(Qt.blue)
        painter.drawRect(0, 0, self._size, self._size)


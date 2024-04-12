from typing import List

from PyQt5.QtWidgets import QLabel, QWidget,  QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPen, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from CustomWidgets.bezier_points_widget import BezierAnchorPointWidget, BezierControlPointWidget
from Models.app_models import (BezierMask,
                               BezierCurve,
                               AppModel)


class BezierMaskWidget(QWidget):
    mousePressSignal = pyqtSignal(int, int)
    mouseReleaseSignal = pyqtSignal(int, int)
    mouseDoubleClickSignal = pyqtSignal(int, int)
    mouseMoveSignal = pyqtSignal(int, int)

    def __init__(self, parent):
        super(BezierMaskWidget, self).__init__()
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.green))
        self.setPalette(palette)
        self.label = QLabel(self)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 600, 600)
        self.view.show()

        self.__anchor_widget1: BezierAnchorPointWidget = None
        self.__anchor_widget2: BezierAnchorPointWidget = None
        self.__control_widget1: BezierControlPointWidget = None
        self.__control_widget2: BezierControlPointWidget = None

        default_plot = QPixmap(600, 600)
        default_plot.fill(Qt.green)
        self.__currentPixmapOfPlot = self.scene.addPixmap(default_plot)

        # Объекты которые нужно перериосвывать каждый кадр (стирать и рисовать заново)
        self.__temps_objects_on_scene = []


# TODO: Событие колеса мыши необходимо перенести сюда
    def mousePressEvent(self, event):
        self.mousePressSignal.emit(event.x(), event.y())

    def mouseMoveEvent(self, event):
        self.mouseMoveSignal.emit(event.x(), event.y())

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickSignal.emit(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.mouseReleaseSignal.emit(event.x(), event.y())

    def draw_mask(self,
                  spline: BezierMask,
                  app_model: AppModel) -> None:
        self.__draw_points_widgets(spline.bezier_curve, app_model)
        self.__draw_bottom_line_of_mask(spline)
        self.__draw_top_line_of_mask(spline)
        self.__draw_border_between_section(spline)
        self.__drawControlLines(spline.bezier_curve)


    def update_solar_plot(self, plot: QPixmap) -> None:
        self.__currentPixmapOfPlot.setPixmap(plot)

    def update_spline(self, spline: BezierMask) -> None:
        self.__clear_current_mask()
        self.__updatePositionPointsWidgets(spline.bezier_curve)
        self.__draw_bottom_line_of_mask(spline)
        self.__draw_top_line_of_mask(spline)
        self.__draw_border_between_section(spline)

        #for i in range(30):
        #    self.__drawTestSlices(spline, i)

        self.__drawControlLines(spline.bezier_curve)

    """
    def __draw_test_slices(self, bezier_mask: BezierMask, offset):
        points: List[QPoint] = bezier_mask.getSliceOfMaskSpline(offset)

        pen = QPen(Qt.blue, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        for i in range(len(points) - 1):
            p1: QPoint = points[i]
            p2: QPoint = points[i + 1]
            newLine = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
            self.__temps_objects_on_scene.append(newLine)
            """

    def __draw_bottom_line_of_mask(self, bezier_mask: BezierMask):
        points_of_bottom_border_mask: List[QPoint] = bezier_mask.get_bottom_border()
        pen = QPen(Qt.yellow, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        for i in range(len(points_of_bottom_border_mask) - 1):
            p1: QPoint = points_of_bottom_border_mask[i]
            p2: QPoint = points_of_bottom_border_mask[i + 1]
            new_line = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
            self.__temps_objects_on_scene.append(new_line)

    def __draw_top_line_of_mask(self, bezier_mask: BezierMask):
        points_of_top_border_mask: List[QPoint] = bezier_mask.get_top_border()
        pen = QPen(Qt.yellow, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        for i in range(len(points_of_top_border_mask) - 1):
            p1: QPoint = points_of_top_border_mask[i]
            p2: QPoint = points_of_top_border_mask[i + 1]
            new_line = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
            self.__temps_objects_on_scene.append(new_line)


    def __draw_border_between_section(self, bezier_mask: BezierMask):
        points_of_top_border_mask: List[QPoint] = bezier_mask.get_top_border()
        points_of_bottom_border_mask: List[QPoint] = bezier_mask.get_bottom_border()

        pen = QPen(Qt.yellow, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        new_line = self.scene.addLine(points_of_bottom_border_mask[0].x(),
                                      points_of_bottom_border_mask[0].y(),
                                      points_of_top_border_mask[0].x(),
                                      points_of_top_border_mask[0].y(),
                                      pen)

        self.__temps_objects_on_scene.append(new_line)

        new_line = self.scene.addLine(points_of_bottom_border_mask[len(points_of_bottom_border_mask) - 1].x(),
                                      points_of_bottom_border_mask[len(points_of_bottom_border_mask) - 1].y(),
                                      points_of_top_border_mask[len(points_of_bottom_border_mask) - 1].x(),
                                      points_of_top_border_mask[len(points_of_bottom_border_mask) - 1].y(),
                                      pen)

        self.__temps_objects_on_scene.append(new_line)

        pen = QPen(Qt.white, 1.0, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin)
        for i in range(1, len(points_of_bottom_border_mask) - 1):
            p1: QPoint = points_of_top_border_mask[i]
            p2: QPoint = points_of_bottom_border_mask[i]
            new_line = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
            self.__temps_objects_on_scene.append(new_line)

    def __draw_points_widgets(self,
                              bezier_curve: BezierCurve,
                              app_model: AppModel) -> None:
        p0 = bezier_curve.points[0]
        p1 = bezier_curve.points[1]
        p2 = bezier_curve.points[2]
        p3 = bezier_curve.points[3]

        self.__anchor_widget1 = BezierAnchorPointWidget(p0, app_model)
        self.__control_widget1 = BezierControlPointWidget(p1, app_model)
        self.__control_widget2 = BezierControlPointWidget(p2, app_model)
        self.__anchor_widget2 = BezierAnchorPointWidget(p3, app_model)

        self.scene.addItem(self.__anchor_widget1)
        self.scene.addItem(self.__control_widget1)
        self.scene.addItem(self.__anchor_widget2)
        self.scene.addItem(self.__control_widget2)


    def __clear_current_mask(self) -> None:
        for item in self.__temps_objects_on_scene:
            self.scene.removeItem(item)

        self.__temps_objects_on_scene.clear()

    def __drawControlLines(self, bezier_curve: BezierCurve) -> None:
        p0: QPoint = bezier_curve.points[0]
        p1: QPoint = bezier_curve.points[1]
        p2: QPoint = bezier_curve.points[2]
        p3: QPoint = bezier_curve.points[3]

        pen = QPen(Qt.red, 3.0, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)

        control_line1 = self.scene.addLine(p0.x(), p0.y(), p1.x(), p1.y(), pen)
        control_line2 = self.scene.addLine(p3.x(), p3.y(), p2.x(), p2.y(), pen)

        self.__temps_objects_on_scene.append(control_line1)
        self.__temps_objects_on_scene.append(control_line2)

    def __updatePositionPointsWidgets(self, bezier_curve: BezierCurve) -> None:
        p0: QPoint = bezier_curve.points[0]
        p1: QPoint = bezier_curve.points[1]
        p2: QPoint = bezier_curve.points[2]
        p3: QPoint = bezier_curve.points[3]

        self.__anchor_widget1.setPos(p0)
        self.__control_widget1.setPos(p1)
        self.__control_widget2.setPos(p2)
        self.__anchor_widget2.setPos(p3)

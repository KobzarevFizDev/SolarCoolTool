import math
from typing import List

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout, QGridLayout, QGraphicsScene, \
    QGraphicsView, QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette, QColor
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from CustomWidgets.curve_point_widget import CurvePointWidget
from CustomWidgets.mask_spline_points_widget import AnchorPointWidget, ControlPointWidget
from Models.solar_editor_model import MaskSplineModel, BezierCurve, SolarEditorModel


class CurveAreaWidget(QWidget):
    mousePressSignal = pyqtSignal(int, int)
    mouseReleaseSignal = pyqtSignal(int, int)
    mouseDoubleClickSignal = pyqtSignal(int, int)
    mouseMoveSignal = pyqtSignal(int, int)

    def __init__(self, parent):
        super(CurveAreaWidget, self).__init__()
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.red))
        self.setPalette(palette)
        self.label = QLabel(self)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 600, 600)
        self.view.show()

        self.__anchorWidget1: AnchorPointWidget = None
        self.__anchorWidget2: AnchorPointWidget = None
        self.__controlWidget1: ControlPointWidget = None
        self.__controlWidget2: ControlPointWidget = None

        # Объекты которые нужно перериосвывать каждый кадр (стирать и рисовать заново)
        self.__tempsObjectsOnScene = []


# TODO: Событие колеса мыши необходимо перенести сюда
    def mousePressEvent(self, event):
        self.mousePressSignal.emit(event.x(), event.y())

    def mouseMoveEvent(self, event):
        self.mouseMoveSignal.emit(event.x(), event.y())

    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickSignal.emit(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.mouseReleaseSignal.emit(event.x(), event.y())

    def drawMask(self,
                 spline: MaskSplineModel,
                 solarEditorModel: SolarEditorModel) -> None:
        self.__drawPointsWidgets(spline.getCurveAtIndex(0), solarEditorModel)
        self.__drawBottomLineOfMask(spline)
        self.__drawTopLineOfMask(spline)
        self.__drawBorderBetweenSection(spline)
        self.__drawControlLines(spline.getCurveAtIndex(0))


    def updateSpline(self, spline: MaskSplineModel) -> None:
        self.__clearCurrentMask()
        self.__updatePositionPointsWidgets(spline.getCurveAtIndex(0))
        self.__drawBottomLineOfMask(spline)
        self.__drawTopLineOfMask(spline)
        self.__drawBorderBetweenSection(spline)
        self.__drawControlLines(spline.getCurveAtIndex(0))


    def __drawBottomLineOfMask(self, maskSpline: MaskSplineModel):
        pointsOfBottomBorderMask: List[QPoint] = maskSpline.getPointsOfBottomBorder()
        for i in range(len(pointsOfBottomBorderMask) - 1):
            p1: QPoint = pointsOfBottomBorderMask[i]
            p2: QPoint = pointsOfBottomBorderMask[i + 1]
            newLine = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y())
            self.__tempsObjectsOnScene.append(newLine)

    def __drawTopLineOfMask(self, maskSpline: MaskSplineModel):
        pointsOfTopBorderMask: List[QPoint] = maskSpline.getPointsOfTopBorder()
        for i in range(len(pointsOfTopBorderMask) - 1):
            p1: QPoint = pointsOfTopBorderMask[i]
            p2: QPoint = pointsOfTopBorderMask[i + 1]
            newLine = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y())
            self.__tempsObjectsOnScene.append(newLine)

    def __drawBorderBetweenSection(self, maskSpline: MaskSplineModel):
        pointsOfTopBorderMask: List[QPoint] = maskSpline.getPointsOfTopBorder()
        pointsOfBottomBorderMask: List[QPoint] = maskSpline.getPointsOfBottomBorder()
        for i in range(len(pointsOfBottomBorderMask)):
            p1: QPoint = pointsOfTopBorderMask[i]
            p2: QPoint = pointsOfBottomBorderMask[i]
            newLine = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y())
            self.__tempsObjectsOnScene.append(newLine)

    def __drawPointsWidgets(self,
                            bezierCurve: BezierCurve,
                            solarEditorModel: SolarEditorModel) -> None:
        p0 = bezierCurve.points[0]
        p1 = bezierCurve.points[1]
        p2 = bezierCurve.points[2]
        p3 = bezierCurve.points[3]

        self.__anchorWidget1 = AnchorPointWidget(p0, solarEditorModel)
        self.__controlWidget1 = ControlPointWidget(p1, solarEditorModel)
        self.__controlWidget2 = ControlPointWidget(p2, solarEditorModel)
        self.__anchorWidget2 = AnchorPointWidget(p3, solarEditorModel)

        self.scene.addItem(self.__anchorWidget1)
        self.scene.addItem(self.__controlWidget1)
        self.scene.addItem(self.__anchorWidget2)
        self.scene.addItem(self.__controlWidget2)


    def __clearCurrentMask(self) -> None:
        for item in self.__tempsObjectsOnScene:
            self.scene.removeItem(item)

        self.__tempsObjectsOnScene.clear()

    def __drawControlLines(self, bezierCurve: BezierCurve) -> None:
        p0: QPoint = bezierCurve.points[0]
        p1: QPoint = bezierCurve.points[1]
        p2: QPoint = bezierCurve.points[2]
        p3: QPoint = bezierCurve.points[3]

        controlLine1 = self.scene.addLine(p0.x(), p0.y(), p1.x(), p1.y())
        controlLine2 = self.scene.addLine(p3.x(), p3.y(), p2.x(), p2.y())

        self.__tempsObjectsOnScene.append(controlLine1)
        self.__tempsObjectsOnScene.append(controlLine2)

    def __updatePositionPointsWidgets(self, bezierCurve: BezierCurve) -> None:
        p0: QPoint = bezierCurve.points[0]
        p1: QPoint = bezierCurve.points[1]
        p2: QPoint = bezierCurve.points[2]
        p3: QPoint = bezierCurve.points[3]

        self.__anchorWidget1.setPos(p0)
        self.__controlWidget1.setPos(p1)
        self.__controlWidget2.setPos(p2)
        self.__anchorWidget2.setPos(p3)

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
        self.view.setGeometry(0 ,0, 600, 600)
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

    def drawSplineCurve(self, spline: MaskSplineModel, resolution: int, solarEditorModel: SolarEditorModel):
        for i in range(spline.numberOfCurves):
            bezierCurve = spline.getCurveAtIndex(i)
            self.__drawBezierCurve(bezierCurve, resolution, solarEditorModel)

    # TODO: Обновлять положение контролов и перерисовывать линию 
    def updateSplineCurve(self, spline: MaskSplineModel, resolution: int):
        for item in self.__tempsObjectsOnScene:
            self.scene.removeItem(item)

        for i in range(spline.numberOfCurves):
            bezierCurve = spline.getCurveAtIndex(i)
            p0: QPoint = bezierCurve.points[0]
            p1: QPoint = bezierCurve.points[1]
            p2: QPoint = bezierCurve.points[2]
            p3: QPoint = bezierCurve.points[3]
            self.__anchorWidget1.setPos(p0)
            self.__controlWidget1.setPos(p1)
            self.__controlWidget2.setPos(p2)
            self.__anchorWidget2.setPos(p3)

            newLine = self.scene.addLine(p0.x(), p0.y(), p1.x(), p1.y())
            self.__tempsObjectsOnScene.append(newLine)

            newLine = self.scene.addLine(p3.x(), p3.y(), p2.x(), p2.y())
            self.__tempsObjectsOnScene.append(newLine)

            for i in range(resolution - 1):
                t1 = 1/resolution * i
                t2 = 1/resolution * (i+1)

                p1: QPoint = bezierCurve.pointAtT(t1)
                p2: QPoint = bezierCurve.pointAtT(t2)

                newLine = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y())
                self.__tempsObjectsOnScene.append(newLine)



    def __drawBezierCurve(self,
                          bezierCurve: BezierCurve,
                          resolution: int,
                          solarEditorModel: SolarEditorModel):
        anchor1: QPoint = bezierCurve.points[0]
        control1: QPoint = bezierCurve.points[1]
        control2: QPoint = bezierCurve.points[2]
        anchor2: QPoint = bezierCurve.points[3]

        self.__anchorWidget1, self.__controlWidget1 = self.__drawBezierCurveController(anchor1,
                                                                                       control1,
                                                                                       solarEditorModel)

        self.__anchorWidget2, self.__controlWidget2 = self.__drawBezierCurveController(anchor2,
                                                                                       control2,                                                                             solarEditorModel)

        # TODO: Дублирование кода
        for i in range(resolution - 1):
            t1 = 1/resolution * i
            t2 = 1/resolution * (i+1)

            p1: QPoint = bezierCurve.pointAtT(t1)
            p2: QPoint = bezierCurve.pointAtT(t2)

            newLine = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y())
            self.__tempsObjectsOnScene.append(newLine)


    def __drawBezierCurveController(self,
                                    anchorPointModel: QPoint,
                                    controlPointModel: QPoint,
                                    solarEditorModel: SolarEditorModel) -> (AnchorPointWidget, ControlPointWidget):
        # TODO: их нужно создать один раз а не перерисовывать каждый раз
        anchorPointWidget = AnchorPointWidget(anchorPointModel, solarEditorModel)
        controlPointWidget = ControlPointWidget(controlPointModel, solarEditorModel)

        newLine = self.scene.addLine(anchorPointModel.x(),
                                     anchorPointModel.y(),
                                     controlPointModel.x(),
                                     controlPointModel.y())

        self.__tempsObjectsOnScene.append(newLine)

        self.scene.addItem(anchorPointWidget)
        self.scene.addItem(controlPointWidget)

        return anchorPointWidget, controlPointWidget


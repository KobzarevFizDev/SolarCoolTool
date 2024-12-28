from typing import List, Tuple

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget,  QGraphicsScene, QGraphicsView, QPushButton
from PyQt5.QtGui import QPen, QPalette, QColor, QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from TimeDistancePlotBuilder.CustomWidgets.bezier_points_widget import BezierAnchorPointWidget, BezierControlPointWidget
from TimeDistancePlotBuilder.Models.app_models import (BezierMask,
                               BezierCurve,
                               AppModel)


class BezierMaskWidget(QWidget):
    mouse_press_signal = pyqtSignal(int, int)
    mouse_release_signal = pyqtSignal(int, int)
    mouse_double_click_signal = pyqtSignal(int, int)
    mouse_move_signal = pyqtSignal(int, int)
    mouse_wheel_signal = pyqtSignal(int)
    export_signal = pyqtSignal(QWidget)

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
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        view_rect = self.contentsRect()
        self.view.setSceneRect(0, 0, view_rect.width(), view_rect.height())

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

        self.__export_button: QPushButton = self.__create_export_button()

        self.__selected_color = Qt.green
        self.__unselected_color = Qt.yellow

    def __create_export_button(self) -> QPushButton:
        export_button = QPushButton("Export", self)
        export_button.clicked.connect(self.__on_export_button_clicked)
        return export_button
    
    def __on_export_button_clicked(self) -> None:
        self.export_signal.emit(self)

# TODO: Событие колеса мыши необходимо перенести сюда
    def mousePressEvent(self, event):
        self.mouse_press_signal.emit(event.x(), event.y())

    def mouseMoveEvent(self, event):
        self.mouse_move_signal.emit(event.x(), event.y())

    def mouseDoubleClickEvent(self, event):
        self.mouse_double_click_signal.emit(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.mouse_release_signal.emit(event.x(), event.y())

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        self.mouse_wheel_signal.emit(a0.angleDelta().y())

    def create_bezier_mask_tool(self,
                                spline: BezierMask,
                                app_model: AppModel) -> None:
        self.__draw_points_widgets(spline.bezier_curve, app_model)
        for i in range(spline.number_of_segments):
            is_selected: bool = app_model.selected_bezier_segments.status_of_segment(i)
            self.__draw_bezier_segment(spline, i, is_selected)
        self.__draw_control_lines(spline.bezier_curve)


    def update_background(self, background: QPixmap) -> None:
        self.__currentPixmapOfPlot.setPixmap(background)

    def update_bezier_mask(self, spline: BezierMask, app_model: AppModel) -> None:
        self.__clear_current_mask()
        self.__update_position_points_widgets(spline.bezier_curve)

        # self.__draw_sections(spline)

        for i in range(spline.number_of_segments):
            is_selected: bool = app_model.selected_bezier_segments.status_of_segment(i)
            self.__draw_bezier_segment(spline, i, is_selected)

        self.__draw_control_lines(spline.bezier_curve)

    def __draw_sections(self, spline: BezierMask): 
        sections: List[Tuple[QPoint, QPoint]] = spline.get_slices(15,is_uniformly=True)
        pen = QPen(Qt.red, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  
        for section in sections:
            bp: QPoint = section[0]
            tp: QPoint = section[1]
            line = self.scene.addLine(bp.x(), bp.y(), tp.x(), tp.y(), pen)
            self.__temps_objects_on_scene.append(line)


    def __draw_bezier_segment(self, bezier_mask: BezierMask, index: int, is_selected: bool) -> None:
        is_first = index == 0
        is_last = bezier_mask.number_of_segments - 1 == index

        if is_first == False and is_last == False:
            self.draw_middle_bezier_segment(bezier_mask, index, is_selected)
        elif is_first == True:
            self.draw_start_bezier_segment(bezier_mask, index, is_selected)
        elif is_last == True:
            self.draw_end_bezier_segment(bezier_mask, index, is_selected)


    def draw_start_bezier_segment(self, bezier_mask: BezierMask, index: int, is_selected: bool) -> None:
        bottom_points: List[QPoint] = bezier_mask.get_bottom_border()
        top_points: List[QPoint] = bezier_mask.get_top_border()

        segment_color = self.__get_segment_color(is_selected)
        pen = QPen(segment_color, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)    

        bp1: QPoint = bottom_points[index]
        bp2: QPoint = bottom_points[index + 1]

        tp1: QPoint = top_points[index]
        tp2: QPoint = top_points[index + 1]

        l1 = self.scene.addLine(tp1.x(), tp1.y(), bp1.x(), bp1.y(), pen)
        l2 = self.scene.addLine(tp1.x(), tp1.y(), tp2.x(), tp2.y(), pen)
        l3 = self.scene.addLine(bp1.x(), bp1.y(), bp2.x(), bp2.y(), pen)

        self.__temps_objects_on_scene.append(l1)
        self.__temps_objects_on_scene.append(l2)
        self.__temps_objects_on_scene.append(l3)


    def draw_middle_bezier_segment(self, bezier_mask: BezierMask, index: int, is_selected: bool) -> None:
        bottom_points: List[QPoint] = bezier_mask.get_bottom_border()
        top_points: List[QPoint] = bezier_mask.get_top_border()
        
        bp1: QPoint = bottom_points[index]
        bp2: QPoint = bottom_points[index + 1]

        tp1: QPoint = top_points[index]
        tp2: QPoint = top_points[index + 1]

        segment_color = self.__get_segment_color(is_selected)

        pen = QPen(segment_color, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)    
        between_section_pen = QPen(Qt.white, 1.0, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin)
        l1 = self.scene.addLine(bp1.x(), bp1.y(), tp1.x(), tp1.y(), between_section_pen)  
        l2 = self.scene.addLine(tp1.x(), tp1.y(), tp2.x(), tp2.y(), pen)  
        l3 = self.scene.addLine(bp2.x(), bp2.y(), bp1.x(), bp1.y(), pen)  

        self.__temps_objects_on_scene.append(l1)
        self.__temps_objects_on_scene.append(l2)
        self.__temps_objects_on_scene.append(l3)

    def draw_end_bezier_segment(self, bezier_mask: BezierMask, index: int, is_selected: bool) -> None:
        bottom_points: List[QPoint] = bezier_mask.get_bottom_border()
        top_points: List[QPoint] = bezier_mask.get_top_border()

        segment_color = self.__get_segment_color(is_selected)
        pen = QPen(segment_color, 2.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  
        between_section_pen = QPen(Qt.white, 1.0, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin)  

        bp1: QPoint = bottom_points[index]
        bp2: QPoint = bottom_points[index + 1]

        tp1: QPoint = top_points[index]
        tp2: QPoint = top_points[index + 1]

        l1 = self.scene.addLine(tp2.x(), tp2.y(), bp2.x(), bp2.y(), pen)
        l2 = self.scene.addLine(tp1.x(), tp1.y(), tp2.x(), tp2.y(), pen)
        l3 = self.scene.addLine(bp2.x(), bp2.y(), bp1.x(), bp1.y(), pen)
        l4 = self.scene.addLine(tp1.x(), tp1.y(), bp1.x(), bp1.y(), between_section_pen)

        self.__temps_objects_on_scene.append(l1)
        self.__temps_objects_on_scene.append(l2)
        self.__temps_objects_on_scene.append(l3)
        self.__temps_objects_on_scene.append(l4)

    def __get_segment_color(self, is_selected: bool):
        return self.__selected_color if is_selected else self.__unselected_color 

            
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

    def __draw_control_lines(self, bezier_curve: BezierCurve) -> None:
        p0: QPoint = bezier_curve.points[0]
        p1: QPoint = bezier_curve.points[1]
        p2: QPoint = bezier_curve.points[2]
        p3: QPoint = bezier_curve.points[3]

        pen = QPen(Qt.red, 3.0, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)

        control_line1 = self.scene.addLine(p0.x(), p0.y(), p1.x(), p1.y(), pen)
        control_line2 = self.scene.addLine(p3.x(), p3.y(), p2.x(), p2.y(), pen)

        self.__temps_objects_on_scene.append(control_line1)
        self.__temps_objects_on_scene.append(control_line2)

    def __update_position_points_widgets(self, bezier_curve: BezierCurve) -> None:
        p0: QPoint = bezier_curve.points[0]
        p1: QPoint = bezier_curve.points[1]
        p2: QPoint = bezier_curve.points[2]
        p3: QPoint = bezier_curve.points[3]

        self.__anchor_widget1.setPos(p0)
        self.__control_widget1.setPos(p1)
        self.__control_widget2.setPos(p2)
        self.__anchor_widget2.setPos(p3)

    def show_export_button(self) -> None:
        self.__export_button.show()

    def hide_export_button(self) -> None:
        self.__export_button.hide()


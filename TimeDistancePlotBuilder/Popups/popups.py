from typing import Optional

import importlib.resources as resources

import numpy.typing as npt
import numpy as np
import imageio

from typing import List

from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QTextEdit, QPushButton, QMessageBox, QSpacerItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

from TimeDistancePlotBuilder.Exceptions.exceptions import IncorrectPathForExport, FileNameIsEmpty

from TimeDistancePlotBuilder.Models.app_models import SolarFrame

class LoadingProgramPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TimeDistancePlotBuilder")
        self.setModal(True)

        layout = QVBoxLayout(self)

        horizontal_container = QHBoxLayout()
        layout.addLayout(horizontal_container)

        with resources.path("TimeDistancePlotBuilder.Resources", "tdpb_logo.png") as logo_path:
            logo_pixmap = QPixmap(str(logo_path))
            logo_pixmap = logo_pixmap.scaled(500, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            self.logo_image = QLabel(self)
            self.logo_image.setPixmap(logo_pixmap)

        self.__loaded_files = QTextEdit(self)
        self.__loaded_files.setReadOnly(True)
        self.__loaded_files.setFixedWidth(200)
        self.__loaded_files.setFixedHeight(300)
        horizontal_container.addWidget(self.logo_image)
        horizontal_container.addWidget(self.__loaded_files) 

        self.__progress_bar = QProgressBar(self)
        self.__progress_bar.setRange(0, 100)
        layout.addWidget(self.__progress_bar)

    def update_progress(self, current_loaded_file: int, limit_of_load_files: int, loaded_file: str):
        self.__loaded_files.append(loaded_file)
        progress = int(float(current_loaded_file) / limit_of_load_files * 100)
        self.__progress_bar.setValue(progress)

class ProcessPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Please wait!")
        self.setModal(True)

        container = QVBoxLayout()

        self.__process_description_label = QLabel("Building time distance plot")
        self.__progress_bar = QProgressBar(self)
        self.__progress_bar.setRange(0, 100)
        
        container.addWidget(self.__process_description_label)
        container.addWidget(self.__progress_bar)

        self.setLayout(container)

    def activate(self, process_description: str) -> None:
        self.show()
        self.__progress_bar.setValue(0)
        self.__process_description_label.setText(process_description)

    def update_progress(self, progress: int) -> None:
        self.__progress_bar.setValue(progress)

# todo: Вынести базовый класс
class ExportTdpPopup(QDialog):
    exception_occured = pyqtSignal(Exception)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export result")
        self.setModal(True)

        self.__path_to_save: Optional[str] = None
        self.__tdp_as_numpy: Optional[npt.NDArray] = None
        self.__frames_for_mp4: Optional[SolarFrame] = None
        self.__tdp_as_png: Optional[QPixmap] = None

        container = QVBoxLayout()

        input_filename_container: QVBoxLayout = self.__create_input_filename_container()
        export_as_png_container: QVBoxLayout = self.__create_export_as_png_container()
        export_as_numpy_container: QVBoxLayout = self.__create_export_as_numpy_array()
        export_video_container: QVBoxLayout = self.__create_export_video_as_mp4()
        buttons_container: QHBoxLayout = self.__create_buttons()

        container.addLayout(input_filename_container)
        container.addLayout(export_as_png_container)
        container.addLayout(export_as_numpy_container)
        container.addLayout(export_video_container)
        container.addLayout(buttons_container)

        self.setLayout(container)

    def __create_input_filename_container(self) -> QVBoxLayout:
        container = QVBoxLayout()
        title_label = QLabel("Input name for save: ")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        horizontal_container = QHBoxLayout()
        self.__base_path_label = QLabel("/base_path/")
        self.__input_name_for_save = QLineEdit("example")

        self.__input_name_for_save.textChanged.connect(self.__update_paths_for_export_files)

        horizontal_container.addWidget(self.__base_path_label)
        horizontal_container.addWidget(self.__input_name_for_save)

        container.addWidget(title_label)
        container.addLayout(horizontal_container)
        return container
    
    def __update_paths_for_export_files(self, name: str) -> None:
        numpy_filename = f"{self.__path_to_save}\\{name}.npy"
        png_filename = f"{self.__path_to_save}\\{name}.png"
        mp4_filename = f"{self.__path_to_save}\\{name}.mp4"

        self.__path_to_export_as_png.setText(png_filename)
        self.__path_to_export_as_numpy.setText(numpy_filename)
        self.__path_to_export_as_video.setText(mp4_filename)

    def __create_export_as_png_container(self) -> QVBoxLayout:
        export_as_png_container = QVBoxLayout()
        path_to_save_as_png_container = QHBoxLayout()
        
        title = QLabel("TDP as png image")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.__tdp_as_png_preview = QLabel()
        self.__path_to_export_as_png = QLabel()

        self.__tdp_as_png_preview.setMaximumSize(400, 100)

        export_as_png_container.addWidget(title)
        export_as_png_container.addWidget(self.__tdp_as_png_preview)
        export_as_png_container.addLayout(path_to_save_as_png_container)

        path_to_save_as_png_container.addWidget(self.__path_to_export_as_png)

        return export_as_png_container
    
    def __create_export_as_numpy_array(self) -> QVBoxLayout:
        export_as_numpy_container = QVBoxLayout()
        path_to_save_as_numpy_container = QHBoxLayout()

        title = QLabel("TDP as numpy array")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.__tdp_as_numpy_preview = QLabel()
        self.__path_to_export_as_numpy = QLabel()

        export_as_numpy_container.addWidget(title)
        export_as_numpy_container.addWidget(self.__tdp_as_numpy_preview)
        export_as_numpy_container.addLayout(path_to_save_as_numpy_container)

        path_to_save_as_numpy_container.addWidget(self.__path_to_export_as_numpy)

        return export_as_numpy_container
    

    def __create_export_video_as_mp4(self) -> QVBoxLayout:
        export_as_video_container = QVBoxLayout()
        path_to_save_as_video_container = QHBoxLayout()

        title = QLabel("Animation of loop as mp4")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.__tdp_as_video_preview = QLabel()
        self.__path_to_export_as_video = QLabel()

        self.__tdp_as_video_preview.setMaximumSize(400, 100)

        export_as_video_container.addWidget(title)
        export_as_video_container.addWidget(self.__tdp_as_video_preview)
        export_as_video_container.addLayout(path_to_save_as_video_container)

        path_to_save_as_video_container.addWidget(self.__path_to_export_as_video)

        return export_as_video_container
    
    def __create_buttons(self) -> QHBoxLayout:
        container = QHBoxLayout()
        
        self.__cancel_button = QPushButton("Cancel")
        self.__export_button = QPushButton("Export")

        self.__cancel_button.clicked.connect(self.close)
        self.__export_button.clicked.connect(self.__export)

        container.addWidget(self.__cancel_button)
        container.addWidget(self.__export_button)

        return container


    def activate(self, 
                 tdp_as_numpy_array: npt.NDArray, 
                 tdp_as_image: QPixmap,
                 frames_for_mp4: List[npt.NDArray],
                 path_to_save: str) -> None:
        self.__path_to_save = path_to_save
        self.__tdp_as_png = tdp_as_image
        self.__frames_for_mp4 = frames_for_mp4
        self.__tdp_as_numpy = tdp_as_numpy_array

        self.__path_to_export_as_png.setText(f"{path_to_save}\\")
        self.__path_to_export_as_numpy.setText(f"{path_to_save}\\")
        self.__path_to_export_as_video.setText(f"{path_to_save}\\")
        self.__tdp_as_png_preview.setPixmap(self.__tdp_as_png)

        with resources.path("TimeDistancePlotBuilder.Resources", "numpy_logo.png") as path_to_numpy_logo:
            numpy_logo_pixmap = QPixmap(str(path_to_numpy_logo))
            self.__tdp_as_numpy_preview.setPixmap(numpy_logo_pixmap)

        with resources.path("TimeDistancePlotBuilder.Resources", "mp4_logo.jpg") as path_to_mp4_logo:
            mp4_logo_pixmap = QPixmap(str(path_to_mp4_logo))
            mp4_logo_pixmap = mp4_logo_pixmap.scaled(400, 100)
            self.__tdp_as_video_preview.setPixmap(mp4_logo_pixmap)
            
        self.show()

        self.__update_paths_for_export_files(self.__input_name_for_save.text())


    def __export(self) -> None:
        try:
            self.__export_as_numpy()
            self.__export_as_png()
            self.__export_animation_loop_as_mp4()
            
        except Exception as e:
            self.exception_occured.emit(e)
        finally:
            self.close()

    # todo: Обработка ошибок. 
    def __export_as_numpy(self) -> None:
        path: str = self.__path_to_export_as_numpy.text()
        np.save(path, self.__tdp_as_numpy)

    def __export_as_png(self) -> None:
        path: str = self.__path_to_export_as_png.text()
        self.__tdp_as_png.save(path)


    def __export_animation_loop_as_mp4(self) -> None:
        path: str = self.__path_to_export_as_video.text()

        with imageio.get_writer(path, fps=5) as writer:
            for frame in self.__frames_for_mp4:
                writer.append_data(frame)


class ExportImagePopup(QDialog):
    exception_occured = pyqtSignal(Exception)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TimeDistancePlotBuilder")
        self.setModal(True)

        self.__image_for_save: Optional[QPixmap] = None 
        self.__path_to_save: Optional[str] = None

        png_export_file_container = QHBoxLayout()

        self.__preivew_image_for_export = QLabel()
        self.__image_filename_label = QLabel()
        self.__image_filename_input = QLineEdit()   
     
        png_export_file_container.addWidget(self.__image_filename_label)
        png_export_file_container.addWidget(self.__image_filename_input)

        container = QVBoxLayout()
        container.addWidget(self.__preivew_image_for_export)
        container.addLayout(png_export_file_container)

        buttons_container = QHBoxLayout()

        self.__cancel_button = QPushButton("Cancel")
        self.__export_button = QPushButton("Export")

        self.__export_button.clicked.connect(self.__export_image)
        self.__cancel_button.clicked.connect(self.__cancel)

        buttons_container.addWidget(self.__cancel_button)
        buttons_container.addWidget(self.__export_button)
        
        container.addLayout(buttons_container)

        self.setLayout(container)

    def activate(self, image_for_save: QPixmap, path_to_save: str) -> None:
        self.__image_for_save: QPixmap = image_for_save
        self.__path_to_save: str = path_to_save
        preview_image = image_for_save.scaled(300, 300)
        self.__preivew_image_for_export.setPixmap(preview_image)
        self.__image_filename_label.setText(f"{path_to_save}\\")
        self.show()

    def __path_is_valid(self, path: str) -> bool:
        return len(path) > 0 

    def __export_image(self) -> None:
        try:
            file_name: str = self.__image_filename_input.text()
            path_to_export = f"{self.__path_to_save}\\{file_name}"
            if (not self.__image_for_save == None) and self.__path_is_valid(file_name):
                self.__image_for_save.save(path_to_export)
            else:
                raise IncorrectPathForExport(path_to_export)
        
        except Exception as e:
            self.exception_occured.emit(e)
        
        finally:    
            self.__cancel()

    def __cancel(self) -> None:
        self.close()
   

class PopupManager:
    def __init__(self, parent_window = None):
        self.__loading_program_popup = LoadingProgramPopup(parent_window)
        self.__export_image_popup = ExportImagePopup(parent_window)
        self.__process_popup = ProcessPopup(parent_window)
        self.__export_tdp_popup = ExportTdpPopup(parent_window)

        self.__exception_popup: QMessageBox = self.__create_exception_popup(parent_window)
        self.__export_image_popup.exception_occured.connect(self.__on_handle_exception)

    def __create_exception_popup(self, parent_window) -> QMessageBox:
        exception_popup = QMessageBox(parent_window)
        exception_popup.setIcon(QMessageBox.Critical)
        exception_popup.setWindowTitle("Error")
        exception_popup.setInformativeText("An error occured")
        return exception_popup

    @property
    def loading_program_popup(self) -> LoadingProgramPopup:
        return self.__loading_program_popup

    @property
    def export_image_popup(self) -> ExportImagePopup:
        return self.__export_image_popup
    
    @property
    def process_popup(self) -> ProcessPopup:
        return self.__process_popup
    
    @property
    def export_tdp_popup(self) -> ExportTdpPopup:
        return self.__export_tdp_popup
    
    def __on_handle_exception(self, exception: Exception) -> None:
        self.__exception_popup.setInformativeText(str(exception))
        self.__exception_popup.show()
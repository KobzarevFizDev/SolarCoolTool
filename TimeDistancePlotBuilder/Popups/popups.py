import os
from typing import Optional

from PyQt5.QtWidgets import QDialog, QProgressDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


from TimeDistancePlotBuilder.Exceptions.exceptions import IncorrectPathForExport

class LoadingProgramPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TimeDistancePlotBuilder")
        self.setModal(True)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "../Resources/tdpb_logo.png") 
        
        layout = QVBoxLayout(self)

        horizontal_container = QHBoxLayout()
        layout.addLayout(horizontal_container)

        logo_pixmap = QPixmap(logo_path)
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


class ExportImagePopup(QDialog):
    exception_occured = pyqtSignal(Exception)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TimeDistancePlotBuilder")
        # self.setModal(True)

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
    
    def __on_handle_exception(self, exception: Exception) -> None:
        self.__exception_popup.setInformativeText(str(exception))
        self.__exception_popup.show()
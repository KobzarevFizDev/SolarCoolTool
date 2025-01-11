import os

from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LoadingPopup(QDialog):
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

        self.loaded_files = QTextEdit(self)
        self.loaded_files.setReadOnly(True)
        self.loaded_files.setFixedWidth(200)
        self.loaded_files.setFixedHeight(300)
        horizontal_container.addWidget(self.logo_image)
        horizontal_container.addWidget(self.loaded_files) 

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

    def update_progress(self, current_loaded_file: int, limit_of_load_files: int, loaded_file: str):
        self.loaded_files.append(loaded_file)
        progress = int(float(current_loaded_file) / limit_of_load_files * 100)
        self.progress_bar.setValue(progress)



class ExportImagePopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TimeDistancePlotBuilder")
        self.setModal(True)

        png_export_file_container = QHBoxLayout()

        self.png_filename_label = QLabel()
        self.png_filename_input = QLineEdit()        
        png_export_file_container.addWidget(self.png_filename_label)
        png_export_file_container.addWidget(self.png_filename_input)


        container = QVBoxLayout()
        container.addLayout(png_export_file_container)

        self.setLayout(container)

    def activate(image_for_save: QPixmap, path_to_save: str) -> None:
        pass
   

class PopupManager:
    def __init__(self, parent_window = None):
        self.__loading_popup = LoadingPopup(parent_window)
        self.__export_image_popup = ExportImagePopup(parent_window)


    @property
    def loading_popup(self) -> LoadingPopup:
        return self.__loading_popup

    @property
    def export_image_popup(self) -> ExportImagePopup:
        return self.__export_image_popup
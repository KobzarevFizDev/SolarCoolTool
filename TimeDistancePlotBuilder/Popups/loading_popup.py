import os

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LoadingPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TimeDistancePlotBuilder")
        # self.setFixedSize(300, 120)
        self.setModal(True)

        current_dir = os.path.dirname(os.path.abspath(__file__))  # Текущая папка
        logo_path = os.path.join(current_dir, "../Resources/tdpb_logo.png")  # Путь к логотипу
        
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


        # layout.addWidget(self.label)


        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

    def update_progress(self, progress: int, loaded_file: str):
        self.progress_bar.setValue(progress)
        self.loaded_files.append(loaded_file)
        print(f"LoadingPopup::update_progress({progress, loaded_file})")
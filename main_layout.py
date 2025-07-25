from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel

from output_widget import  OutputWidget


from input_widget import InputWidget

from PySide6.QtCore import Qt

from settings import settings
from backend import Backend
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel

class MainLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)

        self.backend = Backend()

        self.head_layout = QHBoxLayout()
        self.addLayout(self.head_layout)

        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.jpg")
        logo_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        self.head_layout.addWidget(logo_label)

        company_name_label = QLabel(f"{settings.company_name}")
        company_name_label.setAlignment(Qt.AlignCenter)
        company_name_label.setStyleSheet("font: bold 24pt;")
        self.head_layout.addWidget(company_name_label)

        app_title_label = QLabel("Stairs App")
        app_title_label.setAlignment(Qt.AlignCenter)
        app_title_label.setStyleSheet("font: bold 24pt;")
        self.head_layout.addWidget(app_title_label)

        app_version_label = QLabel(f"v{settings.__version__}")
        app_version_label.setAlignment(Qt.AlignCenter)
        app_version_label.setStyleSheet("font: bold 12pt;")
        self.head_layout.addWidget(app_version_label)



        self.central_layout = QHBoxLayout()
        self.addLayout(self.central_layout)

        # self.central_layout.addLayout(self.input_layout)

        
        self.output_widget = OutputWidget(self.backend)
        self.backend.set_output_widget(self.output_widget)

        self.input_widget = InputWidget(self.backend)
        self.backend.set_input_widget(self.input_widget)
        
        self.central_layout.addWidget(self.input_widget)

        self.central_layout.addWidget(self.output_widget)




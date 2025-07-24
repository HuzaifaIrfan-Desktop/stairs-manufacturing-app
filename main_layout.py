from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel

from output_widget import  OutputWidget


from input_widget import InputWidget

from PySide6.QtCore import Qt

from backend import Backend

class MainLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)

        self.backend = Backend()

        self.head_layout = QHBoxLayout()
        self.addLayout(self.head_layout)

        title_label = QLabel("Stairs App")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: bold 24pt;")
        self.head_layout.addWidget(title_label)

        version_label = QLabel("v0.1.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font: bold 12pt;")
        self.head_layout.addWidget(version_label)



        self.central_layout = QHBoxLayout()
        self.addLayout(self.central_layout)

        # self.central_layout.addLayout(self.input_layout)
        self.input_widget = InputWidget(self.backend)
        self.central_layout.addWidget(self.input_widget)

        self.output_widget = OutputWidget(self.backend)
        self.central_layout.addWidget(self.output_widget)

        self.backend.set_input_widget(self.input_widget)
        self.backend.set_output_widget(self.output_widget)

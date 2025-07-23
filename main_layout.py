from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel

from output_widget import  OutputWidget


from input_widget import InputWidget

from PySide6.QtCore import Qt

from backend import Backend

class MainLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)
        self.central_layout = QHBoxLayout()
        self.addLayout(self.central_layout)

        self.backend = Backend()

        # self.input_layout = InputLayout(self.backend)

        # self.central_layout.addLayout(self.input_layout)
        self.input_widget = InputWidget(self.backend)
        self.central_layout.addWidget(self.input_widget)

        self.output_widget = OutputWidget(self.backend)
        self.central_layout.addWidget(self.output_widget)

        self.backend.set_input_widget(self.input_widget)
        self.backend.set_output_widget(self.output_widget)

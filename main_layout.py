from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel

from output_layout import OutputLayout


from input_layout import InputLayout

from PySide6.QtCore import Qt

class MainLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)
        self.central_layout = QHBoxLayout()
        self.addLayout(self.central_layout)

        self.input_layout = InputLayout()

        self.central_layout.addLayout(self.input_layout)

        self.output_layout = OutputLayout()
        self.central_layout.addLayout(self.output_layout)



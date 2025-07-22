
from occ_viewer import OCCViewerWidget, get_shape_from_file  # Assuming this is a custom module for OCC Viewer


from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
)
class OutputWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(600)
        

        layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        layout.setAlignment(Qt.AlignTop)  
        # self.setLayout(layout)

        self.label = QLabel("Output will be displayed here.")
        layout.addWidget(self.label)

        self.label = QLabel("Output will be displayed here.")
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Add more widgets or layouts as needed


class OutputLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)
        self.occ_viewer = OCCViewerWidget(size=(400, 300))  # Initialize the OCC Viewer widget
        self.addWidget(self.occ_viewer)

        self.addWidget(OutputWidget())

        self.display_3d_model("output/test.obj")  # Load a default model
        
    def display_3d_model(self, file_path: str):

        shape=get_shape_from_file(file_path)

        self.occ_viewer.display.EraseAll()
        self.occ_viewer.display.DisplayShape(shape, update=True)
        self.occ_viewer.display.FitAll()
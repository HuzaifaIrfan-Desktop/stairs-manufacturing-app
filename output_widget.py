
from occ_viewer import OCCViewerWidget, get_shape_from_file  # Assuming this is a custom module for OCC Viewer


from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
)

from backend import Backend
from PySide6.QtWidgets import QMessageBox

class OutputWidget(QWidget):
    def __init__(self, backend:Backend):
        super().__init__()
        self.backend = backend

        self.setFixedWidth(600)
        

        layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        layout.setAlignment(Qt.AlignTop)  
        # self.setLayout(layout)

        self.occ_viewer = OCCViewerWidget(size=(400, 300))  # Initialize the OCC Viewer widget
        layout.addWidget(self.occ_viewer)


        self.label = QLabel("Output Console.")
        self.label.setStyleSheet("font: bold 12pt;")
        layout.addWidget(self.label)
        self.console_area = QTextEdit()
        self.console_area.setReadOnly(True)
        self.console_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.console_area)


        self.setLayout(layout)

        self.display_3d_model("output/test.stl")  # Load a default model
        
    def display_3d_model(self, file_path: str):

        shape=get_shape_from_file(file_path)

        self.occ_viewer.display.EraseAll()
        self.occ_viewer.display.DisplayShape(shape, update=True)
        self.occ_viewer.display.FitAll()

    def clear_console(self):
        self.console_area.clear()

    def append_to_console(self, text: str):
        self.console_area.append(text)
        self.console_area.verticalScrollBar().setValue(self.console_area.verticalScrollBar().maximum())


    def show_popup(self, message: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.show()
        # msg_box.exec()
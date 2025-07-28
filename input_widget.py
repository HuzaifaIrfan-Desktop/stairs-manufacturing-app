
from importlib.resources import path
import json

from pyparsing import line
from models.job.job_params import JobInputParams
from job.job import Job

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy,
)
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel, QFileDialog
import os

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QLineEdit, QSpinBox, QCheckBox, QWidget, QFormLayout, QDoubleSpinBox
from PySide6.QtGui import QFont


from job import available_job_classes
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QScrollArea, QWidget, QFrame



def spacer_widget_for_field(title: str = "", tooltip: str = "") -> QWidget:
    """Creates a widget with a label and a horizontal line under it."""
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    
    label = QLabel(title)
    label.setStyleSheet("font-weight: bold;")
    label.setToolTip(tooltip)
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)

    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setStyleSheet("color: #888; background-color: #888;")  # Set line color
    layout.addWidget(line)

    return container


def widget_for_field(field_type):

    if field_type is str:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Enter text")
        line_edit.setMaxLength(100)
        # line_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return line_edit
    elif field_type is int:
        spin_box = QSpinBox()
        spin_box.setMinimum(0)  # Set a minimum value if needed
        spin_box.setMaximum(999)  # Set a maximum value if needed
        # spin_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return spin_box
    elif field_type is float:
        double_spin_box = QDoubleSpinBox()
        double_spin_box.setMinimum(0)  # Set a minimum value if needed
        double_spin_box.setMaximum(999)  # Set a maximum value if needed
        # double_spin_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return double_spin_box
    elif field_type is bool:
        check_box = QCheckBox()
        # check_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return check_box
    else:
        line_edit = QLineEdit()  # fallback
        line_edit.setPlaceholderText("Unsupported type, enter text")
        line_edit.setStyleSheet("color: red;")  # Indicate unsupported type
        line_edit.setMaxLength(100)
        # line_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return line_edit
    

from backend import Backend


class InputWidget(QWidget):
    def __init__(self, backend:Backend):
        super().__init__()
        self.backend = backend
        self.setFixedWidth(600)
        self.job_params: JobInputParams = JobInputParams()
        self.job_input_params_class = JobInputParams

        self.job: Job = None

        self.inputs = {}



        layout = QVBoxLayout(self)


        input_title_label = QLabel("Job Input")
        input_title_label.setAlignment(Qt.AlignCenter)
        input_title_label.setStyleSheet("font: bold 12pt;")
        layout.addWidget(input_title_label)

        # Add buttons for loading and calculating and saving job
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Load")
        self.load_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.load_button.clicked.connect(self.load_job)
        self.calculate_and_save_button = QPushButton("Calculate and Save")
        self.calculate_and_save_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.calculate_and_save_button.clicked.connect(self.calculate_and_save_job)
        self.open_output_dir_button = QPushButton("Open Outputs")
        self.open_output_dir_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.open_output_dir_button.clicked.connect(self.open_output_directory)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.calculate_and_save_button)
        button_layout.addWidget(self.open_output_dir_button)
        layout.addLayout(button_layout)



        export_button_layout = QHBoxLayout()
        self.export_drawings_button = QPushButton("Export Drawings")
        self.export_drawings_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.export_drawings_button.clicked.connect(self.export_drawings)
        self.export_reports_button = QPushButton("Export Reports")
        self.export_reports_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.export_reports_button.clicked.connect(self.export_reports)
        self.export_cam_button = QPushButton("Export CAM")
        self.export_cam_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.export_cam_button.clicked.connect(self.export_cam)
        export_button_layout.addWidget(self.export_drawings_button)
        export_button_layout.addWidget(self.export_reports_button)
        export_button_layout.addWidget(self.export_cam_button)
        layout.addLayout(export_button_layout)

        # Add a label and a combo box for selecting the job class

        job_class_label =QLabel("Job Class:")
        job_class_label.setStyleSheet("font: bold 12pt;")
        layout.addWidget(job_class_label)
        
        self.job_class_selector = QComboBox()
        self.job_class_selector.addItems([job_class['label'] for job_class in available_job_classes.values()])
        self.job_class_selector.currentTextChanged.connect(self.on_job_class_changed)
        self.selected_job_class_label = None
        # self.job_class_selector.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.job_class_selector.setMinimumWidth(300)
        layout.addWidget(self.job_class_selector)


        # Input Form Layout
        
        # Add a scroll area for the form layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.form_widget = QWidget()

        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self.form_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.scroll_area.setWidget(self.form_widget)
        layout.addWidget(self.scroll_area)
        # layout.addLayout(self.form_layout)



        # self.submit_btn = QPushButton("Submit")
        # self.submit_btn.clicked.connect(self.on_submit)
        # layout.addWidget(self.submit_btn)

        self.info_label = QLabel("Info:")
        self.info_label.setStyleSheet("font: bold 12pt;")
        layout.addWidget(self.info_label)

        self.on_job_class_changed(self.job_class_selector.currentText())
        self.disable_export_buttons()


    def on_job_class_changed(self, job_class_name):
        self.selected_job_class_label = job_class_name
        job_class_key = [key for key, value in available_job_classes.items() if value['label'] == job_class_name][0]
        # self.job_class = available_job_classes[job_class_key]['job_class']
        self.input_params_class = available_job_classes[job_class_key]['input_params_class']
        self.job_params = self.input_params_class()

        self.build_form_from_job_params()

        # self.job = self.job_class(self.job_params)
        
        if self.job_params.job_name:
            loaded_3d_model_path = os.path.join(os.getcwd(), 'output', self.job_params.job_name , f"{self.job_params.job_name}.stl")
            self.backend.display_3d_model(loaded_3d_model_path)


    def build_form_from_job_params(self):
          # Clear existing rows
        # print(f"Building form for {self.form_layout.rowCount()}")
        # remove all existing rows in the form layout in reverse order
        for i in range(self.form_layout.rowCount()-1, -1, -1):
            self.form_layout.removeRow(i)

        self.inputs.clear()
        for name, field in self.input_params_class.model_fields.items():
            
            if name == 'job_class_name':
                continue

            if "spacer" in name:
                widget = spacer_widget_for_field(title=f"{field.description}", tooltip=name)
                self.form_layout.addRow(widget)
                continue


            # print(f"Adding field {field.json_schema_extra}")
            if field.json_schema_extra:
                if 'enum' in field.json_schema_extra:
                    # print(f"Adding field {name} with enum {field.json_schema_extra['enum']}")
                    widget = QComboBox()
                    widget.addItems(field.json_schema_extra['enum'])
                else:
                    widget = widget_for_field(field.annotation)
            else:
                widget = widget_for_field(field.annotation)

            widget_label=QLabel(name)

            if field.description:
                widget.setToolTip(field.description)
                widget_label.setText(field.description)
                widget_label.setToolTip(name)

            self.inputs[name] = widget
            self.form_layout.addRow(widget_label, widget) 

            if hasattr(self.job_params, name):
                value = getattr(self.job_params, name)
                if isinstance(widget, QLineEdit):
                    widget.setText(str(value))
                elif isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
                elif isinstance(widget, QComboBox):
                    index = widget.findText(str(value))
                    if index != -1:
                        widget.setCurrentIndex(index)
        self.disable_export_buttons()              

    def build_job_params_from_form(self):
        data = {}
        for name, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                data[name] = widget.text()
            elif isinstance(widget, QSpinBox):
                data[name] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                data[name] = widget.value()
            elif isinstance(widget, QCheckBox):
                data[name] = widget.isChecked()
            elif isinstance(widget, QComboBox):
                data[name] = widget.currentText()
        try:
            self.job_params = self.input_params_class(**data)
            self.info_label.setText(f"Valid: {self.job_params}")
            self.backend.append_to_console(f"Valid job params: {self.job_params}")
        except Exception as e:
            # self.info_label.setText(f"Error: {e}")
            self.backend.append_to_console(f"Error building job params: {e}")

    def load_job(self):
        
        file_selector = QFileDialog(self)
        file_selector.setDirectory(os.path.join(os.getcwd(), 'output'))
        file_selector.setNameFilter("JSON files (*.json)")
        file_selector.setAcceptMode(QFileDialog.AcceptOpen)
        if file_selector.exec_() == QFileDialog.Accepted:
            file_path = file_selector.selectedFiles()[0]
            with open(file_path, 'r') as f:
                data = json.load(f)
                job_class_name=data["job_class_name"]

                label=available_job_classes[job_class_name]['label']
                self.job_class_selector.setCurrentText(label)
                self.job_params = self.input_params_class(**data)
                # self.info_label.setText(f"Loaded: {self.job_params}") 
                print(f"Loaded job params: {self.job_params}")
                self.backend.append_to_console(f"Loaded job params: {self.job_params}")
        
        self.build_form_from_job_params()

        if self.job_params.job_name:
            loaded_3d_model_path = os.path.join(os.getcwd(), 'output', self.job_params.job_name , f"{self.job_params.job_name}.stl")
            self.backend.display_3d_model(loaded_3d_model_path)

    def set_info_label(self, text):
        self.info_label.setText(text)

    def disable_export_buttons(self):
        self.export_drawings_button.setEnabled(False)
        self.export_reports_button.setEnabled(False)
        self.export_cam_button.setEnabled(False)

    def enable_export_buttons(self):
        self.export_drawings_button.setEnabled(True)
        self.export_reports_button.setEnabled(True)
        self.export_cam_button.setEnabled(True)




    def export_drawings(self):
        self.backend.export_drawings()

    def export_reports(self):
        self.backend.export_reports()

    def export_cam(self):
        self.backend.export_cam()

    def calculate_and_save_job(self):
        self.build_job_params_from_form()
        self.backend.calculate_and_save_job(self.job_params)



    def open_output_directory(self):
        output_dir = os.path.join(os.getcwd(), 'output', self.job_params.job_name)
        if os.path.exists(output_dir):
            if os.name == 'nt':
                os.startfile(output_dir)
            elif os.name == 'posix':
                import subprocess
                subprocess.Popen(['xdg-open', output_dir])
            elif os.name == 'mac':
                import subprocess
                subprocess.Popen(['open', output_dir])
        else:
            self.backend.append_to_console(f"Output directory does not exist: {output_dir}")
            print(f"Output directory does not exist: {output_dir}")


from models.job.job_params import JobInputParams
from job.job import Job

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
)
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel

from output_layout import OutputLayout

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QLineEdit, QSpinBox, QCheckBox, QWidget, QFormLayout, QDoubleSpinBox

from job import available_job_templates
from PySide6.QtWidgets import QComboBox


def widget_for_field(field_type):
    if field_type is str:
        line_edit = QLineEdit()
        # line_edit.setPlaceholderText("Enter text")
        # line_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return line_edit
    elif field_type is int:
        spin_box = QSpinBox()
        # spin_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return spin_box
    elif field_type is float:
        double_spin_box = QDoubleSpinBox()
        # double_spin_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return double_spin_box
    elif field_type is bool:
        check_box = QCheckBox()
        # check_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return check_box
    else:
        line_edit = QLineEdit()  # fallback
        # line_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return line_edit

class JobInputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(600)
        self.job_params: JobInputParams = JobInputParams()

        self.job_class = Job
        self.input_params_class = JobInputParams

        self.job: Job = None

        self.inputs = {}



        layout = QVBoxLayout(self)

        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Load Job")
        self.load_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.load_button.clicked.connect(self.load_job)
        self.calculate_and_save_button = QPushButton("Calculate and Save Job")
        self.calculate_and_save_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.calculate_and_save_button.clicked.connect(self.calculate_and_save_job)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.calculate_and_save_button)

        layout.addLayout(button_layout)


        self.template_selector = QComboBox()
        self.template_selector.addItems([template['label'] for template in available_job_templates.values()])
        self.template_selector.currentTextChanged.connect(self.on_template_changed)
        self.selected_template_label = None

        self.template_selector.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.template_selector.setMinimumWidth(300)
        layout.addWidget(self.template_selector)

        self.form_layout = QFormLayout()
        self.form_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        layout.addLayout(self.form_layout)



        # self.submit_btn = QPushButton("Submit")
        # self.submit_btn.clicked.connect(self.on_submit)
        # layout.addWidget(self.submit_btn)

        self.result_label = QLabel("Result:")
        layout.addWidget(self.result_label)


    def on_template_changed(self, template_name):
        self.selected_template_label = template_name
        template_key = [key for key, value in available_job_templates.items() if value['label'] == template_name][0]
        self.job_class = available_job_templates[template_key]['job_class']
        self.input_params_class = available_job_templates[template_key]['input_params_class']
        self.job_params = self.input_params_class()

        self.build_form_from_job_params()

        self.job = self.job_class(self.job_params)

    def build_form_from_job_params(self):
          # Clear existing rows
        # print(f"Building form for {self.form_layout.rowCount()}")
        # remove all existing rows in the form layout in reverse order
        for i in range(self.form_layout.rowCount()-1, -1, -1):
            self.form_layout.removeRow(i)



        self.inputs.clear()
        for name, field in self.input_params_class.model_fields.items():
            
            if name == 'job_template':
                continue

            widget = widget_for_field(field.annotation)
            self.inputs[name] = widget
            self.form_layout.addRow(QLabel(name), widget) 

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
        try:
            self.job_params = self.input_params_class(**data)
            self.result_label.setText(f"Valid: {self.job_params}")
        except Exception as e:
            self.result_label.setText(f"Error: {e}")

    def load_job(self):
        pass
    def calculate_and_save_job(self):
        self.build_job_params_from_form()
        self.job = self.job_class(self.job_params)

class InputLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)
        self.setAlignment(Qt.AlignTop)  
        self.setSpacing(10)
        self.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        


        self.input_widget = JobInputWidget()
        self.addWidget(self.input_widget)

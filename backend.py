
from PySide6.QtCore import QObject, Signal

try:
    from input_widget import InputWidget
    from output_widget import OutputWidget
except ImportError as e:
    # print("Error importing widgets. Ensure they are in the same directory as backend.py.")
    # print(e)
    pass

from job import available_job_classes

import json
from models.job.job_params import JobInputParams
from job.job import Job
import threading

class Backend(QObject):


    job_completed = Signal(str)
    job_error = Signal(str)



    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize backend state here
        self.input_widget: InputWidget = None
        self.output_widget: OutputWidget = None
        self.job_completed.connect(self.on_job_completed)
        self.job_error.connect(self.on_job_error)

        self.job:Job = None
        self.job_input_params: JobInputParams = None



    def set_input_widget(self, input_widget):
        from input_widget import InputWidget
        self.input_widget: InputWidget = input_widget


    def set_output_widget(self, output_widget):
        from output_widget import OutputWidget

        self.output_widget: OutputWidget = output_widget



    def append_to_console(self, text: str):
        if self.output_widget:
            self.output_widget.append_to_console(text)
        else:
            print("Output widget is not set. Cannot append to console.")
    
    def clear_console(self):
        if self.output_widget:
            self.output_widget.clear_console()
        else:
            print("Output widget is not set. Cannot clear console.")

    def display_3d_model(self, file_path: str):
        if self.output_widget:
            self.output_widget.display_3d_model(file_path)
        else:
            print("Output widget is not set. Cannot display 3D model.")

    def calculate_and_save_job(self, job_input_params: JobInputParams):
        self.job_input_params = job_input_params
        self.job_class_name = job_input_params.job_class_name
        self.job_class = available_job_classes[self.job_class_name]['job_class']
        self.job_input_params_class = available_job_classes[self.job_class_name]['input_params_class']

        self.append_to_console(f"\nStarting Job Export {self.job_input_params.job_name}.\n")
        self.input_widget.set_info_label(f"Exporting {self.job_input_params.job_name}...")

        thread = threading.Thread(target=self.run_job)
        thread.start()

    def run_job(self):

        try:
            self.job = self.job_class(self.job_input_params)
            

            output_params_model_dump=self.job.get_job_output_params().model_dump_json(indent=4)
            self.append_to_console(f"{output_params_model_dump}.\n\n")
            

            self.job.export()
            self.assembly_model_file_path = self.job.export_assembly()
        except Exception as e:
            print(f"Error during job execution: {str(e)}")
            self.job_error.emit(str(e))
            
            return
            
        # print("Job completed signal emit.")
        self.job_completed.emit(f"{self.job_input_params.job_name} Job Export successfully.")

    def on_job_error(self, error_message: str):
        # Handle job error
        # print("Job error signal received.")

        self.append_to_console(error_message)
        self.append_to_console(f"\nJob {self.job_input_params.job_name} Export Failed.\n\n")
        
        self.output_widget.show_error_popup("Job Export Failed", f"Error during job execution: {error_message}")
        self.input_widget.set_info_label("Job Export Failed")

    def on_job_completed(self, success_message: str):
        # Handle job completion
        # print("Job completed signal received.")
        # self.clear_console()
        
        self.append_to_console(f"{success_message}.\n\n")

        self.output_widget.show_popup("Job Export Successful", success_message)
        self.input_widget.set_info_label("Job Export Successful")

        self.display_3d_model(self.assembly_model_file_path)

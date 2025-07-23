
from PySide6.QtCore import QObject, Signal

try:
    from input_widget import InputWidget
    from output_widget import OutputWidget
except ImportError as e:
    print("Error importing widgets. Ensure they are in the same directory as backend.py.")
    print(e)


class Backend(QObject):
    # Example signal
    dataChanged = Signal(str)



    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize backend state here
        self.input_widget: InputWidget = None
        self.output_widget: OutputWidget = None

    def update_data(self, new_data):
        # Update internal state and emit signal
        self.dataChanged.emit(new_data)

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
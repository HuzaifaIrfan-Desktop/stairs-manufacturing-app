
from PySide6.QtCore import QObject, Signal



class Backend(QObject):
    # Example signal
    dataChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize backend state here

    def update_data(self, new_data):
        # Update internal state and emit signal
        self.dataChanged.emit(new_data)
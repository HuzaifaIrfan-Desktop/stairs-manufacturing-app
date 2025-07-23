from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel
import sys

from main_layout import MainLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stairs App")
        self.resize(800, 600)

        main_layout = MainLayout()

        self.setLayout(main_layout)



from qt_material import apply_stylesheet, list_themes


if __name__ == "__main__":

    app = QApplication(sys.argv)


    print("Available themes:", list_themes())

    # Apply Material Design theme
    apply_stylesheet(app, theme='light_orange.xml')

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

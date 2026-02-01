from ui import MainWindow
import sys
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    APP_VERSION = "1.0.2"
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
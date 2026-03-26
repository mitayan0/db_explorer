# main.py
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from path_utils import initialize_database

if __name__ == "__main__":
    # Ensure the database is initialized in AppData before the app starts
    initialize_database()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # It's better to use sys.exit(app.exec()) as exec is a reserved word in Py3
    sys.exit(app.exec())
import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication

from controller.main_controller import MainController
from gui.main_window import MainWindow
from model.gol_model import GOLModel

app = QApplication(sys.argv)
# Set the dark style for PyQt5
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

# Create the model, GUI and controller
gol_model = GOLModel()
main_window = MainWindow(gol_model)
main_controller = MainController(app, main_window, gol_model)

main_window.show()
sys.exit(app.exec_())

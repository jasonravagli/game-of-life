from PyQt5.QtWidgets import QMainWindow, QMessageBox

import patterns
from gui.grid_widget import GridWidget
from gui.ui_main_window import Ui_MainWindow
from model.gol_model import GOLModel


class MainWindow(QMainWindow):
    def __init__(self, gol_model: GOLModel):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.slider_speed.setValue(gol_model.get_fps())

        # Add the custom widget to the central QFrame to display the current state of the GOL grid
        self.grid_widget = GridWidget(gol_model)
        self.ui.main_grid_layout.addWidget(self.grid_widget, 0, 0)

        # Load the available patterns into the QComboBox
        self.ui.combo_patterns.insertItem(0, "Custom")
        self.ui.combo_patterns.insertItems(1, patterns.get_available_patterns())

        # Register the UI as observer of the GOLSettingsModel to update the controls with its values
        self._gol_model = gol_model
        self._gol_model.observe(self.update_controls)
        self.update_controls()

    def connect_to_button_clear(self, slot):
        self.ui.button_clear.clicked.connect(slot)

    def connect_to_button_load(self, slot):
        self.ui.button_load.clicked.connect(slot)

    def connect_to_button_play(self, slot):
        self.ui.button_play.clicked.connect(slot)

    def connect_to_button_save(self, slot):
        self.ui.button_save.clicked.connect(slot)

    def connect_to_button_step(self, slot):
        self.ui.button_single_step.clicked.connect(slot)

    def connect_to_combo_patterns(self, slot):
        self.ui.combo_patterns.currentTextChanged.connect(slot)

    def connect_to_radio_age(self, slot):
        self.ui.radio_age.toggled.connect(slot)

    def connect_to_slider_speed(self, slot):
        self.ui.slider_speed.valueChanged.connect(slot)

    def reset_combo_patterns(self):
        self.ui.combo_patterns.setCurrentIndex(0)

    def show_error_message(self, message: str):
        """
        Show an error message into a popup dialog

        :param message: THe message to show
        """
        QMessageBox.critical(self, "Error", message)

    def update_controls(self):
        """
        Update the controls of the GUI using the current state and settings of the GOL simulation
        """

        # If the simulation is running disable proper controls
        if self._gol_model.get_running():
            self.ui.button_play.setText("Pause")
            self.ui.button_clear.setEnabled(False)
            self.ui.button_load.setEnabled(False)
            self.ui.button_save.setEnabled(False)
            self.ui.button_single_step.setEnabled(False)
            self.ui.combo_patterns.setEnabled(False)
        else:
            self.ui.button_play.setText("Play")
            self.ui.button_clear.setEnabled(True)
            self.ui.button_load.setEnabled(True)
            self.ui.button_save.setEnabled(True)
            self.ui.button_single_step.setEnabled(True)
            self.ui.combo_patterns.setEnabled(True)

        self.ui.label_fps.setText(f"{self._gol_model.get_fps()} FPS")



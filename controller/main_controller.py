import os

import numpy as np
from PyQt5.QtWidgets import QFileDialog, QApplication
from scipy import ndimage

import patterns
from config import config
from gui.main_window import MainWindow
from model.gol_model import GOLModel
from worker import Worker


class MainController:
    """
    Class representing the controller of the MVC pattern. It connects to the GUI signals to catch the user interactions
    and modify the GOL state model accordingly.
    """

    def __init__(self, application: QApplication, main_window: MainWindow, gol_model: GOLModel):
        self._application = application
        application.aboutToQuit.connect(self._stop_worker_on_app_closing)

        self._main_window = main_window
        main_window.connect_to_button_clear(self.clear_grid)
        main_window.connect_to_button_load(self.load_custom_pattern)
        main_window.connect_to_button_play(self.start_stop)
        main_window.connect_to_button_save(self.save_pattern)
        main_window.connect_to_button_step(self.single_step)
        main_window.connect_to_combo_patterns(self.select_example_pattern)
        main_window.connect_to_radio_age(self.toggle_show_cell_age)
        main_window.connect_to_slider_speed(self.set_speed)
        main_window.grid_widget.connect_to_cell_clicked(self.toggle_cell)

        self._gol_model = gol_model
        self._worker = None

        # Variables for the grid update
        self._conv_filter = np.ones((3, 3))
        self._conv_filter[1, 1] = 0

    def clear_grid(self):
        """
        Clear the GOL grid bringing it back to its initial state (depending on the chosen pattern)
        :return:
        """
        self.select_example_pattern(self._gol_model.get_base_pattern())
        self._main_window.show_message_on_status_bar("Grid cleared")

    def load_custom_pattern(self):
        """
        Load a pattern from a chosen file into the current GOL state
        :return:
        """
        self._main_window.reset_combo_patterns()
        file_path = QFileDialog.getOpenFileName(self._main_window, "Load pattern file", filter="Pattern File (*.cells)")[0]
        if file_path:
            self._load_file(file_path)
            self._main_window.show_message_on_status_bar("Pattern loaded")

    def _load_file(self, file_path: str):
        """
        Helper method to load a pattern from a .cells file (plain text format).

        :param file_path: Path of the pattern file
        :return:
        """
        grid_pattern = patterns.read_pattern_file(file_path)

        grid_height, grid_width = self._gol_model.get_grid_size()
        pattern_height, pattern_width = grid_pattern.shape

        # If the pattern is bigger than the grid show an error
        if pattern_height > grid_height or pattern_width > grid_width:
            self._main_window.show_error_message("The loaded pattern is bigger than the available grid")
        else:
            # Copy the pattern at the center of a blank grid
            new_grid = np.zeros(self._gol_model.get_grid_size(), np.uint8)
            v_margin = (grid_height - pattern_height) // 2
            h_margin = (grid_width - pattern_width) // 2
            new_grid[v_margin:v_margin + pattern_height, h_margin:h_margin + pattern_width] = grid_pattern

            self._gol_model.set_grid_as_numpy(new_grid)

    def save_pattern(self):
        """
        Save the current grid state in a .cells file as a reloadable state
        :return:
        """
        file_path = QFileDialog.getSaveFileName(self._main_window, "Save pattern file", filter="Pattern File (*.cells)")[0]
        if file_path:
            patterns.save_pattern_file(file_path, self._gol_model.get_grid_as_numpy())
            self._main_window.show_message_on_status_bar("Pattern saved")

    def select_example_pattern(self, pattern_name):
        """
        Load a predefined pattern chosen from the provided list
        :param pattern_name: The name of the pattern to load (it is the same of its file name)
        :return:
        """
        self._gol_model.set_base_pattern(pattern_name)
        # The selected pattern is the custom one: restart from a blank grid
        if pattern_name == "Custom":
            new_grid = np.zeros(self._gol_model.get_grid_size(), np.uint8)
            self._gol_model.set_grid_as_numpy(new_grid)
        else:
            file_path = os.path.join(config.ROOT_PATH, config.FOLDER_PATTERNS, pattern_name + ".cells")
            self._load_file(file_path)

    def set_speed(self, speed):
        """
        Change the simulation speed
        :param speed: The simulation speed in FPS
        :return:
        """
        self._gol_model.set_fps(speed)
        if self._gol_model.get_running():
            self._worker.set_wait_time(1 / self._gol_model.get_fps())

    def single_step(self):
        """
        Performs an update step of the grid applying the Game of Life rules.
        Besides calculating dead and living cells at the next time step, it also calculates the age of each cell
        (how many time steps they are alive). The age ranges from 0 (dead) to 255 (ancient)
        """
        grid_curr_age = self._gol_model.get_grid_as_numpy()
        grid_curr_alive = grid_curr_age.astype(np.bool).astype(np.uint8)

        # Use convolution to calculate the number of neighbors for each cell
        grid_neighbors = ndimage.convolve(grid_curr_alive, self._conv_filter, mode="constant", cval=0)

        # Calculate which cells to give birth: a dead cell is born when it has exactly three neighbors
        grid_newborns = grid_neighbors == 3
        grid_newborns = np.logical_and(grid_newborns, np.logical_not(grid_curr_alive))

        # Calculate which cells survive: a living cell survive when it has two or three neighbors
        grid_survived = np.logical_and(grid_neighbors >= 2, grid_neighbors <= 3)
        grid_survived = np.logical_and(grid_survived, grid_curr_alive)

        # Calculate the living cells at the next step merging survived and newborn cells
        grid_next = np.logical_or(grid_newborns, grid_survived).astype(np.uint8)

        # Calculate the age of the cells in the new grid
        grid_next = grid_curr_age * grid_next + grid_next
        np.putmask(grid_next, grid_curr_age == 255,
                   255)  # This is necessary to avoid the overflow handling by numpy and cap the array values to 255

        self._gol_model.set_grid_as_numpy(grid_next)

    def start_stop(self):
        """
        Start the GOL simulation on a separate thread or stop it if it was already running
        """
        if not self._gol_model.get_running():
            self._gol_model.set_running(True)
            self._worker = Worker(self.single_step, 1 / self._gol_model.get_fps())
            self._worker.start()
        else:
            self._worker.stop()
            self._gol_model.set_running(False)

    def _stop_worker_on_app_closing(self):
        if self._worker is not None:
            self._worker.stop()

    def toggle_show_cell_age(self, show_cell_age: bool):
        self._gol_model.set_show_cell_age(show_cell_age)

    def toggle_cell(self, cell_coord: tuple):
        """
        Toggle the state of the specified cell
        :param cell_coord: A tuple containing the cell coordinates as (row, column)
        """

        grid = self._gol_model.get_grid_as_numpy()
        row, col = cell_coord
        grid[row, col] = 0 if grid[row, col] else 1
        self._gol_model.set_grid_as_numpy(grid)

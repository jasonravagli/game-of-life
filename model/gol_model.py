import numpy as np

from model.observable import Observable
from config import config


class GOLModel(Observable):
    """
    Class representing the current state of the Game of Life (the model in the MVC pattern)
    """

    def __init__(self):
        super().__init__()

        # Base pattern from which the current grid state is originated
        self._base_pattern = "Custom"
        # Size of the GOL grid
        self._grid_size = config.GRID_SIZE
        # Current state of the GOL grid. It is a matrix of 8-bit integers where an element represents the current age of
        # the corresponding grid cell (0: dead cell, 255: ancient cell)
        self._grid = np.zeros(self._grid_size, dtype=np.uint8)
        # Speed of the GOL simulation (in frames per second)
        self._fps = config.FPS
        # Flag that indicates if the simulation is currently running
        self._running = False
        # Flag that indicates whether to display the cells age or only their state (dead/alive)
        self._show_cell_age = False

    def get_base_pattern(self) -> str:
        return self._base_pattern

    def get_grid_as_numpy(self) -> np.ndarray:
        """
        Getter method for the current state of the GOL grid
        :return: A copy of the numpy array of the grid, to avoid unintended changes to the GOL grid state
        """
        return self._grid.copy()

    def get_fps(self) -> int:
        return self._fps

    def get_grid_size(self) -> tuple:
        return self._grid_size

    def get_running(self) -> bool:
        return self._running

    def get_show_cell_age(self) -> bool:
        return self._show_cell_age

    def set_base_pattern(self, base_pattern: str):
        self._base_pattern = base_pattern
        self.notify()

    def set_fps(self, value: int):
        self._fps = value
        self.notify()

    def set_grid_size(self, rows: int, cols: int):
        self._grid_size = (rows, cols)
        self._grid = np.zeros(self._grid_size, np.int8)
        self.notify()

    def set_grid_as_numpy(self, grid: np.ndarray):
        self._grid = grid
        self.notify()

    def set_running(self, value: bool):
        self._running = value
        self.notify()

    def set_show_cell_age(self, value: bool):
        self._show_cell_age = value
        self.notify()

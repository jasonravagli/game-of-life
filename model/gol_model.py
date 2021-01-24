import numpy as np

from model.observable import Observable
from config import config


class GOLModel(Observable):
    """
    DESCRIPTION HERE
    """

    def __init__(self):
        super().__init__()

        self._grid_size = config.GRID_SIZE
        self._grid = np.zeros(self._grid_size, dtype=np.uint8)
        self._fps = config.FPS
        self._running = False
        self._show_cell_age = False

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

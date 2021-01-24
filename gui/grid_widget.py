import math

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QLabel, QSizePolicy

import utils
from model.gol_model import GOLModel


class GridWidget(QLabel):

    # Signal to notify the mouse click on a cell of the grid
    cell_clicked = pyqtSignal(tuple)

    def __init__(self, gol_model: GOLModel):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(1, 1)  # To allow the QLabel to shrink also with a pixmap attached

        # Connect to the model and show the initial grid
        self._gol_model = gol_model
        gol_model.observe(self.update_grid)
        self.update_grid()

        # Coordinates of the QPixmap (the grid) upper-left corner inside the QLabel. They are required to handle mouse events on the cells
        self.x_pixmap = 0
        self.y_pixmap = 0

    def connect_to_cell_clicked(self, slot):
        self.cell_clicked.connect(slot)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Slot for the mouse release event on the widget. It allows the user to edit the grid cells.
        Emits the cell_clicked signal sending to the connected slots the coordinates (row, column) of the clicked grid cell.
        :param ev: The mouse event
        """

        # Ignore the mouse click if the simulation is running (the grid is not editable)
        if not self._gol_model.get_running():
            x_click = ev.pos().x()
            y_click = ev.pos().y()

            # Converts the widget coordinates into grid coordinates
            x_grid = x_click - self.x_pixmap
            y_grid = y_click - self.y_pixmap
            if 0 <= x_grid < self.pixmap().width() and 0 <= y_grid < self.pixmap().height():
                grid_size = self._gol_model.get_grid_size()
                row = math.floor(y_grid*grid_size[0]/self.pixmap().height())
                col = math.floor(x_grid*grid_size[1]/self.pixmap().width())

                self.cell_clicked.emit((row, col))

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """
        Slot for the resize event of the widget. It updates the QPixmap coordinates to handle mouse events on the grid
        and repaints the grid to fit the new dimensions
        :param a0:
        :return:
        """
        self.x_pixmap = (self.width() - self.pixmap().width())//2
        self.y_pixmap = (self.height() - self.pixmap().height())//2
        self.update_grid()

    def update_grid(self):
        """
        Update the widget to display the current state of the GOL grid
        """

        # Transform the numpy array of the grid state into an image (QPixmap) to be displayed on the widget
        qimage = utils.numpy_to_qimage(self._gol_model.get_grid_as_numpy(), self._gol_model.get_show_cell_age())
        qpixmap = QPixmap.fromImage(qimage)
        # Scale the created QPixmap to fit the widget
        self.setPixmap(qpixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio))

        # Update the QPixmap coordinates
        self.x_pixmap = (self.width() - self.pixmap().width())//2
        self.y_pixmap = (self.height() - self.pixmap().height())//2

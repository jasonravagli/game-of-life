import math

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget

import utils
from model.gol_model import GOLModel


class GridWidget(QLabel):
    """
    Custom widget to display and edit the current GOL grid state
    """

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
        # Keep track of the last tile drawn to handle continuous drawing through mouse dragging
        self._last_tile_drawn_row = -1
        self._last_tile_drawn_col = -1
        # Flag that indicates whether we are drawing on the grid (the mouse is pressed)
        self._drawing = False

        # To enable the mouseMoveEvent tracking
        QWidget.setMouseTracking(self, True)

    def connect_to_cell_clicked(self, slot):
        self.cell_clicked.connect(slot)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Slot for the mouse move event on the widget.
        When the application is in a drawing session (the mouse is clicked and dragged), toggle the state of all the
        cells where the mouse pass over.
        :param ev: The mouse event
        """
        x_pos = ev.pos().x()
        y_pos = ev.pos().y()

        # Check if the mouse position is inside the effective level grid image
        x_grid = x_pos - self.x_pixmap
        y_grid = y_pos - self.y_pixmap
        if 0 <= x_grid < self.pixmap().width() and 0 <= y_grid < self.pixmap().height() and \
                not self._gol_model.get_running():
            self.setCursor(Qt.CrossCursor)

            # Check if we are drawing (the mouse is pressed and dragged)
            if self._drawing:
                # Converts the widget coordinates into grid coordinates
                grid_size = self._gol_model.get_grid_size()
                row = math.floor(y_grid * grid_size[0] / self.pixmap().height())
                col = math.floor(x_grid * grid_size[1] / self.pixmap().width())

                # Check if the event was already handled for this tile (the mouse is moved over the same tile)
                if row != self._last_tile_drawn_row or col != self._last_tile_drawn_col:
                    self.cell_clicked.emit((row, col))
                    self._last_tile_drawn_row = row
                    self._last_tile_drawn_col = col
        else:
            self.unsetCursor()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Slot for the mouse press event on the widget. It allows the user to edit the grid cells when the simulation is
        not running.
        Emits the cell_clicked signal sending to the connected slots the coordinates (row, column) of the clicked grid cell
        and starts a drawing session (continuous drawing through mouse dragging).
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
                # Converts the widget coordinates into grid coordinates
                grid_size = self._gol_model.get_grid_size()
                row = math.floor(y_grid * grid_size[0] / self.pixmap().height())
                col = math.floor(x_grid * grid_size[1] / self.pixmap().width())

                self.cell_clicked.emit((row, col))
                self._last_tile_drawn_row = row
                self._last_tile_drawn_col = col

                # Start continuous drawing
                self._drawing = True

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        """
        Slot for the mouse release event on the widget.
        Ends the drawing session.
        :param ev: The mouse event
        """

        self._drawing = False
        self._last_tile_drawn_row = -1
        self._last_tile_drawn_col = -1

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

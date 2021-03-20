import numpy as np
from PyQt5.QtGui import QImage

import utils.colors as colors


def numpy_to_qimage(np_array: np.ndarray, show_age: bool):
    """
    Convert the numpy array representing the GOL grid to a QImage.

    :param np_array: Numpy array to be converted
    :param show_age: Whether to show cells ages using progressive color transitions. If False a binary color pattern is used (dead or alive)

    :return: The QImage created from the numpy array
    """

    # Only support 2D array of bytes
    assert len(np_array.shape) == 2 and np_array.dtype == np.uint8

    width = np_array.shape[1]
    height = np_array.shape[0]
    bytes_per_line = width
    image = QImage(np_array, width, height, bytes_per_line, QImage.Format_Indexed8)

    # Maps array values to color
    if show_age:
        image.setColorTable(colors.AGE_COLOR_TABLE)
    else:
        image.setColorTable(colors.BINARY_COLOR_TABLE)

    return image

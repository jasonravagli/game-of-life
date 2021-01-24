"""
Define the colors for the GOL cells
"""
from PyQt5.QtGui import qRgb

ALIVE_COLOR = qRgb(255, 255, 255)
DEAD_COLOR = qRgb(0, 0, 0)

# From light blue (newborn cells) to red (ancient cells)
AGE_COLOR_TABLE = [DEAD_COLOR] + [qRgb(0, 255-i*2, 255) for i in range(128)] +\
                  [qRgb(i*2, 0, 255-i*2) for i in range(127)]
# Alive cell: white - Dead cell: black
BINARY_COLOR_TABLE = [DEAD_COLOR] + [ALIVE_COLOR for i in range(256)]

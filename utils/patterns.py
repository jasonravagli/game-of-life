import os
import numpy as np

from config import config


def get_available_patterns() -> list:
    """
    Search for available GOL classical into the patterns directory. It only considers files with the .cells extension (plain text format).

    :return: A list containing the names of the available GOl examples
    """
    path_folder = os.path.join(config.ROOT_PATH, config.FOLDER_PATTERNS)
    return [f.replace(".cells", "") for f in os.listdir(path_folder) if os.path.isfile(os.path.join(path_folder, f)) and f.endswith(".cells")]


def read_pattern_file(file_path: str) -> np.ndarray:
    """
    Read the pattern from the specified file into a numpy array. The only format supported is plain text (.cells extension)

    :param file_path: The pattern file to load
    :return: The numpy array containing the dead and alive cells of the requested pattern. None if the pattern file is not found
    """

    # Check if the example file exists
    if not os.path.isfile(file_path):
        return None

    rows = 0
    cols = 0
    with open(file_path) as f:
        for i, l in enumerate(f):
            if l[0] != "!":
                rows += 1
                if len(l) > cols:
                    cols = len(l) - 1  # Exclude the end of line char from the column count

    grid = np.zeros((rows, cols), dtype=np.uint8)

    skip_rows = 0
    with open(file_path) as f:
        for j, line in enumerate(f):
            for k, c in enumerate(line):
                if c == "!" and k == 0:
                    skip_rows += 1
                    break
                elif c == "O":
                    grid[j - skip_rows, k] = 1

    return grid


def save_pattern_file(file_path: str, grid_pattern: np.ndarray):
    """
    Write a pattern into a .cells file (using the plain text format)
    :param file_path: The file into which save the pattern
    :param grid_pattern: Numpy array representing the grid state of the pattern
    :return:
    """

    # Transform the grid into a list of string lines
    lines = []
    for row in range(len(grid_pattern)):
        line = ["." if cell == 0 else "O" for cell in grid_pattern[row]]
        line_str = "".join(line) + "\n"
        lines.append(line_str)

    with open(file_path, mode="w") as f:
        f.writelines(lines)



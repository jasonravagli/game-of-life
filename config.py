import os


class Config:

    def __init__(self):
        self.FOLDER_PATTERNS = os.path.join("resources", "patterns")
        self.FPS = 30
        self.GRID_SIZE = (150, 250)
        self.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


config = Config()

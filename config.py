import os


class Config:

    def __init__(self):
        self.FOLDER_PATTERNS = "patterns"
        self.FPS = 30
        self.GRID_SIZE = (150, 300)
        self.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


config = Config()

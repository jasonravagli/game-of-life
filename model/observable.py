from PyQt5.QtCore import QObject, pyqtSignal


class Observable(QObject):
    """
    Object that allows to be notified on its state changes (Observer pattern)
    """
    value_changed = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def observe(self, slot):
        self.value_changed.connect(slot)

    def notify(self):
        self.value_changed.emit(self)

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSettings, pyqtSignal

from .ui import welcome


class Welcome(QWidget, welcome.Ui_Welcome):
    open_file = pyqtSignal(str)
    create_file = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.recent_files.itemDoubleClicked.connect(self.on_recent_clicked)

    def update_recent(self, items):
        self.recent_files.clear()

        for fname, _ in items:
            self.recent_files.addItem(fname)

    def on_recent_clicked(self, item):
        self.open_file.emit(item.text())

    def on_open_file(self):
        self.open_file.emit(None)

    def on_create_file(self):
        self.create_file.emit()

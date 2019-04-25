from PyQt5.QtWidgets import QWidget

from .ui import welcome


class Welcome(QWidget, welcome.Ui_Welcome):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def on_open_file(self):
        pass

    def on_create_file(self):
        pass

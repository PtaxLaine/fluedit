import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSignal
from .ui import welcome
from .editor import Editor


class Welcome(QWidget, welcome.Ui_Welcome):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QMessageBox
from PyQt5 import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from .ui import playground

from .highlighter import Highlighter


class Playground(QWidget, playground.Ui_Playground):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.textHighlighter = Highlighter(self.translited_message_edit)

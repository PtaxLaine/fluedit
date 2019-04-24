import sys
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QMessageBox, QListWidgetItem
from PyQt5 import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QColor, QBrush, QIcon
from .ui import editor_cfg
from .highlighter import Highlighter
from .playground import Playground
import fluent.syntax
import fluent.syntax.ast
import re


class EditorConfig(QWidget, editor_cfg.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

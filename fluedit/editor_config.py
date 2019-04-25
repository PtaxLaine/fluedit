from PyQt5.QtWidgets import QWidget

from .ui import editor_cfg


class EditorConfig(QWidget, editor_cfg.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

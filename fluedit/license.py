import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QToolBox, QStackedWidget, QFileDialog, QMessageBox, QTabWidget, \
    QDialog, QWidget
from PyQt5.QtCore import QSettings, qFatal
from PyQt5.QtGui import QIcon
from .ui import license_dialog
from .welcome import Welcome
from PyQt5.QtCore import pyqtSignal
from .editor import Editor
import sys
import os
import traceback
from . import resource_rc


class LicenseDialog(QDialog, license_dialog.Ui_Dialog):
    accepted = pyqtSignal()
    rejected = pyqtSignal()

    def __init__(self, parent=None, allow_close=False):
        super().__init__(parent)
        self.setupUi(self)

        if parent:
            self.setModal(True)

        if allow_close:
            self.accept_button.hide()
            self.decline_button.hide()
        else:
            self.close_button.hide()

        self.licenses = QToolBox()
        self.lic_layout.addWidget(self.licenses)

        self.__allow_close = allow_close
        self.__accepted = False

        self._init_licenses()

    def _init_licenses(self):
        for lic in self._load_licenses():
            box = QTextEdit()
            box.setReadOnly(True)
            box.setPlainText(lic[1])
            self.licenses.addItem(box, lic[0])

    def _load_licenses(self):
        yield ("fluedit", "All rights reserved")
        yield ("other", "TODO")  # TODO: load licenses

    def on_rejected(self):
        self.rejected.emit()
        self.close()

    def on_accepted(self):
        self.accepted.emit()
        self.__accepted = True
        self.close()

    def closeEvent(self, _ev):
        if not self.__allow_close and not self.__accepted:
            self.rejected.emit()

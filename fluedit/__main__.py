import sys
import traceback

from PyQt5.QtCore import QSettings, qFatal
from PyQt5.QtWidgets import QApplication, QMessageBox

# noinspection PyUnresolvedReferences
from . import resource_rc
from .license import LicenseDialog
from .main import MainWindow


class Starter:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setOrganizationName("ptaxa.net")
        self.app.setApplicationName("FluEdit")
        sys.excepthook = Starter.except_hook

        settings = QSettings()
        if settings.value("license_accepted") != "true":
            self.lic_wnd = LicenseDialog()
            self.lic_wnd.accepted.connect(self.on_license_accepted)
            self.lic_wnd.show()
        else:
            self.main = MainWindow()
            self.main.show()

    def exec(self):
        self.app.exec_()

    def on_license_accepted(self):
        QSettings().setValue("license_accepted", "true")
        self.main = MainWindow()
        self.main.show()

    @staticmethod
    def except_hook(cls, exception, tb):
        sys.__excepthook__(cls, exception, traceback)
        fmt = traceback.format_exception(cls, exception, tb)
        fmt = "\n".join(fmt)
        b = QMessageBox.critical(None, "unexpected exception", fmt,
                                 QMessageBox.Abort | QMessageBox.Ignore,
                                 QMessageBox.Abort)
        if b == QMessageBox.Abort:
            qFatal(fmt)


if __name__ == '__main__':
    Starter().exec()

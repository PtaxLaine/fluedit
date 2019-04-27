import sys
import traceback

from PyQt5.QtCore import QSettings, qFatal
from PyQt5.QtWidgets import QApplication, QMessageBox

# noinspection PyUnresolvedReferences
from . import resource_rc
from .license import LicenseDialog
from .main import MainWindow


def except_hook(cls, exception, tb):
    sys.__excepthook__(cls, exception, traceback)
    fmt = traceback.format_exception(cls, exception, tb)
    fmt = "\n".join(fmt)
    b = QMessageBox.critical(None, "unexpected exception", fmt,
                             QMessageBox.Abort | QMessageBox.Ignore,
                             QMessageBox.Abort)
    if b == QMessageBox.Abort:
        qFatal(fmt)


def _license_accepted():
    MainWindow().show()
    QSettings().setValue("license_accepted", "true")


def main():
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    app.setOrganizationName("ptaxa.net")
    app.setApplicationName("FluEdit")

    settings = QSettings()
    if settings.value("license_accepted") != "true":
        window = LicenseDialog()
        window.accepted.connect(_license_accepted)
        window.show()
    else:
        wnd = MainWindow()
        wnd.show()
    app.exec_()


if __name__ == '__main__':
    main()

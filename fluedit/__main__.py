import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings, qFatal
from PyQt5.QtGui import QIcon
from .ui import mainwindow
from .welcome import Welcome
from .editor import Editor
import sys
import traceback
from . import resource_rc

class ExampleApp(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.welcome = Welcome()
        self.editor = None
        self.layout.addWidget(self.welcome)

        self.welcome.open_file_button.clicked.connect(self.on_open_file)
        self.welcome.create_file_button.clicked.connect(self.on_create_file)
        self.actionOpen.triggered.connect(self.on_open_file)
        self.actionCreate.triggered.connect(self.on_create_file)
        self.actionAboutQt.triggered.connect(QApplication.instance().aboutQt)

        self.open_file("en.ftl")

    def on_open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,
                                              filter="Fluent Translation List (*.ftl);;Any files (*)",
                                              options=options)
        if file:
            self.open_file(file)

    def on_create_file(self):
        self.open_file(None)

    def open_file(self, file):
        if self.welcome:
            self.welcome.deleteLater()
            self.welcome = None
        if self.editor:
            self.editor.deleteLater()
        self.editor = Editor(file)
        self.actionSave.triggered.connect(self.editor.on_save)
        self.actionSave_as.triggered.connect(self.editor.on_save_as)
        self.layout.addWidget(self.editor)
        self.actionFind_message_id.triggered.connect(self.editor.find_msg_id_dialog)
        self.actionFind_message.triggered.connect(self.editor.find_msg_dialog)
        self.actionFindNext.triggered.connect(self.editor.find_next)


def except_hook(cls, exception, tb):
    sys.__excepthook__(cls, exception, traceback)
    fmt = traceback.format_exception(cls, exception, tb)
    fmt = "\n".join(fmt)
    b = QMessageBox.critical(None, "unexpected exception", fmt,
                             QMessageBox.Abort | QMessageBox.Ignore,
                             QMessageBox.Abort)
    if b == QMessageBox.Abort:
        qFatal(fmt)


def main():
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    app.setOrganizationName("ptaxa.net")
    app.setApplicationName("fluedit")
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QTabWidget
from PyQt5.QtCore import QSettings, qFatal
from PyQt5.QtGui import QIcon
from .ui import mainwindow
from .welcome import Welcome
from .editor import Editor
import sys
import os
import traceback
from . import resource_rc


class ExampleApp(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.welcome = Welcome()
        self.layout.addWidget(self.welcome)

        self.editors = []
        self.editor_tabs = QTabWidget()
        self.editor_tabs.hide()
        self.layout.addWidget(self.editor_tabs)

        self.welcome.open_file_button.clicked.connect(self.on_open_file)
        self.welcome.create_file_button.clicked.connect(self.on_create_file)

        self.open_file("en.ftl")

    def closeEvent(self, *args, **kwargs):
        pass  # todo: save file dialog

    def notimplemented(self):
        raise NotImplementedError()

    def on_about_qt(self):
        QApplication.instance().aboutQt()

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

    def on_find_message(self):

        editor = self.current_editor
        if editor:
            editor.find_msg_dialog()

    def on_find_message_id(self):
        editor = self.current_editor
        if editor:
            editor.find_msg_id_dialog()

    def on_find_next(self):
        editor = self.current_editor
        if editor:
            editor.find_next()

    @property
    def current_editor(self):
        if self.editor_tabs:
            return self.editor_tabs.currentWidget()

    def open_file(self, file):
        if file:
            file = os.path.abspath(file)

        self.welcome.hide()
        self.editor_tabs.show()

        if file:
            for x in self.editors:
                if x.filename == file:
                    self.editor_tabs.setCurrentWidget(x)
                    return

        editor = Editor(file)
        self.editor_tabs.addTab(editor, file if file else '~unnamed')
        self.editors.append(editor)
        self.editor_tabs.setCurrentWidget(editor)

        def on_changed():
            i = self.editor_tabs.indexOf(editor)
            text = self.editor_tabs.tabText(i)
            if not text.startswith('* '):
                self.editor_tabs.setTabText(i, f'* {text}')

        def on_saved():
            i = self.editor_tabs.indexOf(editor)
            text = self.editor_tabs.tabText(i)
            if text.startswith('* '):
                self.editor_tabs.setTabText(i, text[1:])

        editor.changed.connect(on_changed)
        editor.saved.connect(on_saved)


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

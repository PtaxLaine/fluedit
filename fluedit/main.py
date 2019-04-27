import os
import time

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTabWidget, QMessageBox, QAction

from .editor import Editor
from .license import LicenseDialog
from .ui import mainwindow
from .welcome import Welcome
from .memoirs import Memoirs


class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.welcome = Welcome()
        self.layout.addWidget(self.welcome)

        self.editor_tabs = QTabWidget()
        self.editor_tabs.hide()
        self.editor_tabs.setDocumentMode(True)
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setMovable(True)
        self.editor_tabs.setTabBarAutoHide(True)
        self.editor_tabs.tabCloseRequested.connect(self.on_close_editor)
        self.editor_tabs.currentChanged.connect(self.on_tab_current_changed)
        self.layout.addWidget(self.editor_tabs)

        self.welcome.open_file.connect(self.on_welcome_open_file)
        self.welcome.create_file.connect(self.on_create_file)

        self.update_recent()

        # self.open_file("./en.ftl")

    def closeEvent(self, ev):
        for _, editor in self._iter_tabs():
            if editor.is_modificated:
                quest = QMessageBox.question(self, '', f'Save file "{editor.filename}"" ?',
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.SaveAll | QMessageBox.Cancel,
                                             QMessageBox.Cancel)

                if quest == QMessageBox.Cancel:
                    ev.ignore()
                    break
                elif quest == QMessageBox.SaveAll:
                    self.on_save_all()
                    break
                elif quest == QMessageBox.Yes:
                    self._save(editor)

    def notimplemented(self):
        raise NotImplementedError()

    def on_find_memoirs(self):
        Memoirs.search_dialog(self)

    def on_import_source(self):
        raise NotImplementedError()

    def on_import_ftl(self):
        raise NotImplementedError()

    def on_tab_current_changed(self, index):
        if index >= 0:
            text = self.editor_tabs.tabText(index)
            self.update_title(text)
        else:
            self.welcome.show()

    def update_title(self, text):
        self.setWindowTitle(f'fluedit \u2013 {text}')

    def on_about_qt(self):
        QApplication.instance().aboutQt()

    def on_welcome_open_file(self, fname):
        if fname:
            self.open_file(fname)
        else:
            self.on_open_file()

    def on_open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,
                                              filter="Fluent Translation List (*.ftl);;Any files (*)",
                                              options=options)
        if file:
            self.open_file(file)

    def show_license(self):
        LicenseDialog(self, True).show()

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

    def on_save(self):
        editor = self.current_editor
        self._save(editor)

    def on_save_as(self):
        editor = self.current_editor
        self._save_as(editor)

    def on_close(self):
        self._close(self.editor_tabs.currentIndex())

    def on_close_all(self):
        while self.editor_tabs.count():
            if not self._close(0):
                break

    def on_close_editor(self, index):
        self._close(index)

    def _close(self, index):
        editor = self.editor_tabs.widget(index)

        quest = None
        if editor.is_modificated:
            quest = QMessageBox.question(self, '', f'Save file "{editor.filename}"" ?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                         QMessageBox.Cancel)
            if quest == QMessageBox.Yes:
                self._save(editor)

        if quest != QMessageBox.Cancel:
            self.editor_tabs.removeTab(index)
        return quest != QMessageBox.Cancel

    def _save(self, editor):
        if editor.filename:
            editor.save_file(editor.filename)
            editor.on_saved()
        else:
            self._save_as(editor)

    def _save_as(self, editor):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getSaveFileName(self,
                                              filter="Fluent Translation List (*.ftl)",
                                              options=options)
        if file:
            if not file.endswith('.ftl'):
                file += '.ftl'
            editor.save_file(file)

        editor.on_saved()

    def on_save_all(self):
        for _, w in self._iter_tabs():
            self._save(w)

    def _iter_tabs(self):
        return map(lambda i: (i, self.editor_tabs.widget(i)),
                   range(self.editor_tabs.count())
                   )

    def update_recent(self):
        settings = QSettings()
        recent = settings.value("recent_files", {})
        recent = list(recent.items())
        recent.sort(key=lambda x: x[1], reverse=True)

        self.welcome.update_recent(recent)

        self.menuOpen_recent.setEnabled(len(recent) > 0)
        self.menuOpen_recent.clear()
        for x in recent[:15]:
            def closure(fname):
                def action():
                    self.open_file(fname)

                act = QAction(fname, self.menuOpen_recent)
                act.triggered.connect(action)
                self.menuOpen_recent.addAction(act)

            closure(x[0])

    @property
    def current_editor(self):
        if self.editor_tabs:
            return self.editor_tabs.currentWidget()

    @staticmethod
    def _append_recent(filename):
        settings = QSettings()
        recent = settings.value("recent_files", {})
        recent[filename] = time.time()
        settings.setValue("recent_files", recent)
        settings.sync()

    def open_file(self, file):
        if file:
            file = os.path.abspath(file)
            self._append_recent(file)

        self.update_recent()

        self.welcome.hide()
        self.editor_tabs.show()

        if file:
            for _, w in self._iter_tabs():
                if w.filename == file:
                    self.editor_tabs.setCurrentWidget(w)
                    return

        editor = Editor(file)
        self.editor_tabs.addTab(editor, file if file else '~unnamed')
        self.editor_tabs.setCurrentWidget(editor)

        def on_changed():
            i = self.editor_tabs.indexOf(editor)
            text = self.editor_tabs.tabText(i)
            if not text.startswith('* '):
                text = f'* {text}'
                self.editor_tabs.setTabText(i, text)
            self.update_title(text)

        def on_saved():
            i = self.editor_tabs.indexOf(editor)
            text = self.editor_tabs.tabText(i)
            if text.startswith('* '):
                self.editor_tabs.setTabText(i, text[1:])

        editor.changed.connect(on_changed)
        editor.saved.connect(on_saved)

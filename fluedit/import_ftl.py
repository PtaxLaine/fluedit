from __future__ import annotations

import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from .common import FTL_FILE_FILTER
from .editor import Editor
from .message import Message


class _FileInput(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.input = QLineEdit(self)
        self.layout.addWidget(self.input)

        self.button = QToolButton(self)
        self.button.setText("...")
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        dir = os.path.dirname(os.path.abspath(self.input.text())) if self.input.text() else None

        fname, _ = QFileDialog.getOpenFileName(self, None, dir, FTL_FILE_FILTER)
        if fname:
            self.input.setText(fname)


class _SelectFile(QWidget):
    def __init__(self, parent: ImportFtl):
        super().__init__(parent)

        self.layout = QFormLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.filename_input = _FileInput(self)
        self.layout.addRow("Filename", self.filename_input)

        self.import_button = QPushButton(self)
        self.import_button.setText("Import into current file")
        self.layout.addRow(None, self.import_button)

        self.import_button.clicked.connect(parent.on_import_button_clicked)


class _ImportWidget(QWidget):
    def __init__(self, parent: ImportFtl):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.imports = QListWidget(self)
        self.layout.addWidget(self.imports)

        self.cleanup_deleted_checkbox = QCheckBox(self)
        self.cleanup_deleted_checkbox.setText("Delete removed messages")
        self.layout.addWidget(self.cleanup_deleted_checkbox)

        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.buttons_layout.addWidget(self.back_button)

        self.done_button = QPushButton(self)
        self.done_button.setText("Done")
        self.buttons_layout.addWidget(self.done_button)

        self.back_button.clicked.connect(parent.on_importer_back)
        self.done_button.clicked.connect(parent.on_done)

    def _add_item(self, msg, status):
        item = QListWidgetItem()
        item.setText(msg[0].key)
        if status == 'new':
            item.setToolTip(f'new message\n"{msg[0].message}"')
            item.setIcon(QIcon(':/icons/list-done.png'))
        elif status == 'updated':
            item.setToolTip(f'updated message\n"{msg[0].message}"\nVS\n"{msg[1].original}"')
            item.setIcon(QIcon(':/icons/list-untranslated.png'))
        elif status == 'removed':
            item.setToolTip("removed message")
            item.setIcon(QIcon(':/icons/list-error.png'))
        self.imports.addItem(item)

    def init_diff(self):
        new_ones, updated, removed = self.parent.diff()

        self.imports.clear()

        for x in new_ones:
            self._add_item(x, 'new')
        for x in updated:
            self._add_item(x, 'updated')
        for x in removed:
            self._add_item(x, 'removed')


class ImportFtl(QDialog):
    def __init__(self, editor: Editor):
        super().__init__(editor)
        self.setModal(True)
        self.setWindowTitle("Import FTL")
        self.resize(300, 100)

        self.editor = editor
        self.filename = None
        self.messages = []
        self.errors = []

        self.layout = QVBoxLayout(self)

        self.select_file = _SelectFile(self)
        self.layout.addWidget(self.select_file)

        self.importer = _ImportWidget(self)
        self.importer.hide()
        self.layout.addWidget(self.importer)

    def diff(self):
        new_ones = []
        updated = []
        removed = []

        editor = self.editor

        for msg in self.messages:
            if msg.key in editor.messages:
                cur = editor.messages[msg.key]
                if msg.message != cur.original:
                    updated.append((msg, cur))
            else:
                new_ones.append((msg,))

        keys = set((x.key for x in self.messages))
        for key, msg in editor.messages.items():
            if key not in keys:
                removed.append((msg,))

        return new_ones, updated, removed

    @staticmethod
    def _read_file(fname):
        with open(fname, 'rb') as fs:
            file = fs.read().decode()
        return Message.parse_file(file)

    def on_done(self):
        cleanup_deleted = self.importer.cleanup_deleted_checkbox.isChecked()

        new_ones, updated, removed = self.diff()

        for msg in new_ones:
            self.editor.append_message(msg[0])

        for msg, cur in updated:
            if cur.original != msg.message:
                if cur.message != msg.message:
                    cur.draft = True
                cur.original = msg.message

        if cleanup_deleted:
            for msg in removed:
                self.editor.delete_message(msg[0])

        self.close()

    def on_importer_back(self):
        self.messages = []
        self.errors = []
        self.filename = None
        self.importer.hide()
        self.select_file.show()
        self.resize(300, 100)

    def on_import_button_clicked(self):
        fname = self.select_file.filename_input.input.text()
        if fname:
            try:
                messages, errors = self._read_file(fname)
            except Exception as err:
                QMessageBox.warning(self, None, str(err))
            else:
                self.errors = errors
                self.messages = messages
                self.filename = fname
                self.select_file.hide()
                self.importer.show()
                self.importer.init_diff()
                self.resize(400, 300)

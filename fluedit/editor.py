from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget, QInputDialog, QMessageBox, QListWidgetItem, QMenu, QAction

from .editor_config import EditorConfig
from .message import Message
from .playground import Playground
from .ui import editor
from .memoirs import Memoirs
import shutil


class Editor(QWidget, editor.Ui_Editor):
    changed = pyqtSignal()
    saved = pyqtSignal()

    def __init__(self, filename):
        super().__init__()
        self.setupUi(self)

        self.messages = {}
        self.find_msg_generator = None
        self.current_message = None
        self.is_modificated = False
        self.filename = filename

        self.messages_list.setContextMenuPolicy(Qt.Qt.CustomContextMenu)
        self.messages_list.customContextMenuRequested.connect(self.on_messages_list_menu)

        self.playground = Playground()
        self.playground.setEnabled(False)
        self.tab_playground_layout.addWidget(self.playground)

        self.config_widget = EditorConfig()
        self.tab_config_layout.addWidget(self.config_widget)

        self.translited_message_edit.error.connect(self.on_fluent_error)
        if filename:
            for msg in self._read_file(filename):
                self.append_message(msg)
            if self.messages:
                self.messages_list.setCurrentRow(0)

    def on_messages_list_menu(self, pos):
        item = self.messages_list.itemAt(pos)
        if item:
            row = self.messages_list.row(item)
            msg = self.messages[item.text()]

            def on_delete():
                quest = QMessageBox.question(self, '', f'Delete message "{msg.key}"?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if quest == QMessageBox.Yes:
                    del self.messages[msg.key]
                    self.messages_list.takeItem(row)
                    self.on_changed()

            def on_rename():
                text, _ = QInputDialog.getText(self, None, "new message id")
                if text:
                    if text in self.messages:
                        v = QMessageBox.warning(self, None, f'item {text} already exist, continue?',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if QMessageBox.No == v:
                            return
                        self._remove_message(text)
                    self._remove_message(msg.key)
                    new = msg.copy(text)
                    self.append_message(new)
                    self.on_changed()

            actions = [
                ("Delete message", on_delete),
                ("Rename message", on_rename),
            ]

            menu = QMenu()
            for name, cb in actions:
                act = QAction(name, menu)
                act.triggered.connect(cb)
                menu.addAction(act)
            menu.exec(self.messages_list.mapToGlobal(pos))

    def on_fluent_error(self, error):
        if self.current_message:
            if error != self.current_message.error:
                self.current_message.error = error

    def on_changed(self):
        self.is_modificated = True
        self.changed.emit()

    def on_tab_changed(self, value):
        if not self.current_message:
            return

        self.playground.setEnabled(value == 1)

        plain = self.playground.translited_message_edit.toPlainText()
        if plain != self.current_message.message:
            v = QMessageBox.question(self, '', f'translated message was benn changed, apply changes?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if v == QMessageBox.Yes:
                self.translited_message_edit.setPlainText(plain)
            else:
                self.playground.translited_message_edit.setPlainText(self.current_message.message)

    def on_fliter_changed(self, text):
        self.messages_list.clear()
        messages = self.messages.values()
        if text == 'Drafts':
            messages = filter(lambda x: x.draft, messages)
        elif text == 'Untranslated':
            messages = filter(lambda x: not x.is_translated, messages)
        elif text == 'Translated':
            messages = filter(lambda x: x.is_translated, messages)
        elif text == 'With comments':
            messages = filter(lambda x: x.comment, messages)
        elif text == 'Without comments':
            messages = filter(lambda x: not x.comment, messages)
        for msg in messages:
            item = self._create_item(msg)
            self.messages_list.addItem(item)
        self.messages_list.setCurrentRow(0)
        current = self.messages_list.currentItem()
        if current:
            self.current_message = self.messages[current.text()]

    def on_draft_box_changed(self, value):
        msg = self.current_message
        if msg:
            draft = value == Qt.Qt.Checked
            if draft != msg.draft:
                msg.draft = draft
                self.on_changed()

    def on_saved(self):
        self.is_modificated = False
        self.saved.emit()

    def on_comment_changed(self):
        if self.current_message:
            plain = self.comments_edit.toPlainText()
            if plain != self.current_message.comment:
                self.current_message.comment = plain
                self.on_changed()

    def on_message_changed(self):
        if self.current_message:
            plain = self.translited_message_edit.toPlainText()
            self.playground.translited_message_edit.setPlainText(plain)
            if self.current_message.message != plain:
                self.on_changed()
                self.current_message.message = plain

    def on_memoirs_activated(self, item):
        text = item.text()
        self.translited_message_edit.setPlainText(text)

    def on_current_row_changed(self, row):
        self.playground.clean()
        item = self.messages_list.item(row)
        if not item:
            return
        item = item.text()
        self.current_message = self.messages[item]
        msg = self.messages[item]
        self.translited_message_edit.setPlainText(msg.message)
        self.comments_edit.setPlainText(msg.comment if msg.comment else "")
        self.original_message_edit.setPlainText(msg.original if msg.original else "")
        self.is_draft_box.setCheckState(Qt.Qt.Checked if msg.draft else Qt.Qt.Unchecked)
        self.msg_source_fname_box.setText(msg.file[0] if msg.file else "")
        self.msg_source_line_box.setText(str(msg.file[1]) if msg.file else "")

        self.memoirs_list.clear()
        if msg.original:
            if msg.is_translated:
                Memoirs.append(msg)

            def completed(variants: (Memoirs.SearchResult,)):
                for v in variants:
                    self.memoirs_list.addItem(v.msg.message)

            Memoirs.search(msg, completed)

    def on_create_message(self):
        text, _ = QInputDialog.getText(self, None, "item name")
        if text:
            if text in self.messages:
                v = QMessageBox.warning(self, None, f'item {text} already exist, continue?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if QMessageBox.No == v:
                    return
                else:
                    for x in self.messages_list.findItems(text, Qt.Qt.MatchExactly):
                        self.messages_list.takeItem(self.messages_list.row(x))
                        break
            msg = Message(text, "", None)
            self.append_message(msg)

    def _remove_message(self, key):
        if key in self.messages:
            for x in self.messages_list.findItems(key, Qt.Qt.MatchExactly):
                row = self.messages_list.row(x)
                self.messages_list.takeItem(row)
            del self.messages[key]

    def save_file(self, filename):
        data = Message.build_file(self.messages.values())
        tmp_file = f'{filename}.tmp'
        with open(tmp_file, 'wb') as fs:
            fs.write(data.encode())
        shutil.move(tmp_file, filename)

    def _read_file(self, filename):
        with open(filename, encoding='UTF-8') as fs:
            file_data = fs.read()
            messages, errors = Message.parse_file(file_data)

            if errors:
                QMessageBox.warning(self, None,
                                    'file load error\n' + '\n'.join(errors))

            return messages

    def _create_item(self, message) -> QListWidgetItem:
        item = QListWidgetItem(message.key)
        self._update_list_item(item, message)
        return item

    def _update_list_item(self, item, message):
        if message.error:
            icon = QIcon(':/icons/list-error.png')
        elif message.draft:
            icon = QIcon(':/icons/list-draft.png')
        elif not message.is_translated:
            icon = QIcon(':/icons/list-untranslated.png')
        else:
            icon = QIcon(':/icons/list-done.png')
        item.setIcon(icon)

    def append_message(self, message, set_current=False):
        self.messages[message.key] = message
        item = self._create_item(message)
        self.messages_list.addItem(item)
        if set_current:
            self.messages_list.setCurrentItem(item)

        def on_changed():
            item = list(self.messages_list.findItems(message.key, Qt.Qt.MatchExactly))
            if item:
                self._update_list_item(item[0], message)

        message.changed.connect(on_changed)

    def find_next(self):
        if self.find_msg_generator:
            try:
                next(self.find_msg_generator)
            except StopIteration:
                QMessageBox.information(self, None, 'messages list end reached')

    def find_msg_id_dialog(self):
        self.find_msg_generator = None
        text, _ = QInputDialog.getText(self, None, "find message by id")
        if text:
            def gen():
                for item in self.messages_list.findItems(text, Qt.Qt.MatchContains):
                    self.messages_list.setCurrentItem(item)
                    yield True

            self.find_msg_generator = gen()
            self.find_next()

    def find_msg_dialog(self):
        self.find_msg_generator = None
        text, _ = QInputDialog.getText(self, None, "find message by translated text")
        if text:
            text = text.lower()

            def gen():
                for message in self.messages.values():
                    if text in message.message.lower():
                        for item in self.messages_list.findItems(message.key, Qt.Qt.MatchExactly):
                            self.messages_list.setCurrentItem(item)
                            yield True

            self.find_msg_generator = gen()
            self.find_next()

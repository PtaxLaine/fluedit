import sys
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QMessageBox, QListWidgetItem
from PyQt5 import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QColor, QBrush, QIcon
from PyQt5.QtCore import pyqtSignal
from .ui import editor
from .highlighter import Highlighter
from .playground import Playground
from .editor_config import EditorConfig
import fluent.syntax
import fluent.syntax.ast
from .message import Message


def build(key, value):
    return key + " = " + value


class Editor(QWidget, editor.Ui_Editor):
    changed = pyqtSignal()
    saved = pyqtSignal()

    def __init__(self, filename):
        super().__init__()
        self.setupUi(self)

        self.playground = Playground()
        self.tab_playground_layout.addWidget(self.playground)

        self.config_widget = EditorConfig()
        self.tab_config_layout.addWidget(self.config_widget)

        self.textHighlighter = Highlighter(self.translited_message_edit)

        self.messages = {}
        self.find_msg_generator = None
        self.current_message = None
        self.is_modificated = False

        self.filename = filename
        if filename:
            self.messages = self.load_file(filename)

        for x in self.messages.values():
            self.messages_list.addItem(self.create_item(x))
        self.messages_list.setCurrentRow(0)
        if self.messages:
            self.current_message = self.messages[self.messages_list.item(0).text()]

    def on_changed(self):
        self.is_modificated = True
        self.changed.emit()

    def load_file(self, filename):
        def offset_to_line(data, offset: int) -> (int, str):
            line = 1
            for i in range(offset):
                if data[i] == '\n':
                    line += 1
            return line, data[offset:].split('\n', 1)[0].strip()

        messages = {}
        with open(filename, encoding='UTF-8') as fs:
            file_data = fs.read()
            syntax = fluent.syntax.FluentParser()
            entries = syntax.parse(file_data)
            for entity in entries.body:
                if isinstance(entity, fluent.syntax.ast.Message):
                    comment = entity.comment.content if entity.comment else None
                    message = file_data[entity.value.span.start:entity.value.span.end]
                    key = entity.id.name
                    messages[key] = Message(key, message, comment)
                elif isinstance(entity, fluent.syntax.ast.Junk):
                    pos = offset_to_line(file_data, entity.span.start)
                    QMessageBox.warning(self, '', 'file load error\n' +
                                        "\n".join(map(lambda x: f'line: {pos[0]}   {x.code}: {x.message}',
                                                      entity.annotations)))
                elif isinstance(entity, fluent.syntax.ast.ResourceComment):
                    pass
                elif isinstance(entity, fluent.syntax.ast.GroupComment):
                    pass
        return messages

    def on_tab_changed(self, value):
        if not self.current_message:
            return

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
            item = self.create_item(msg)
            self.messages_list.addItem(item)

    def on_save(self):
        if self.filename:
            self.save_file(self.filename)
        else:
            self.on_save_as()

    def on_save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getSaveFileName(self,
                                              filter="Fluent Translation List (*.ftl)",
                                              options=options)
        if file:
            if not file.endswith('.ftl'):
                file += '.ftl'
            self.save_file(file)

    def save_file(self, filename):
        raise NotImplementedError()

    def on_draft_box_changed(self, value):
        msg = self.current_message
        if msg:
            draft = value == Qt.Qt.Checked
            if draft != msg.draft:
                msg.draft = draft
                self.on_changed()
                self.update_list_item(self.messages_list.currentItem(), msg)

    def on_comment_changed(self):
        pass

    def on_message_changed(self):
        if self.current_message:
            plain = self.translited_message_edit.toPlainText()
            self.playground.translited_message_edit.setPlainText(plain)
            if self.current_message.message != plain:
                self.on_changed()
                self.current_message.message = plain
                self.update_list_item(self.messages_list.currentItem(), self.current_message)

                # syntax = fluent.syntax.FluentParser()
                # entries = syntax.parse(build("f", plain))
                # for enity in entries.body:
                #     if isinstance(enity, fluent.syntax.ast.Junk):
                #         for ann in enity.annotations:
                #             print(ann.message)
                #             print(ann.args)
                #             print(enity.span)
                # self.textHighlighter.set_error((enity.span.start-4, enity.span.end-4), ann.message)

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
        self.is_draft_box.setCheckState(Qt.Qt.Checked if msg.draft else Qt.Qt.Unchecked)

    def create_item(self, message) -> QListWidgetItem:
        item = QListWidgetItem(message.key)
        self.update_list_item(item, message)
        return item

    def update_list_item(self, item, message):
        icon = QIcon()
        if message.draft:
            icon = QIcon(':/icons/list-draft.png')
        elif not message.is_translated:
            icon = QIcon(':/icons/list-untranslated.png')
        elif message.errors:
            icon = QIcon(':/icons/list-error.png')
        else:
            icon = QIcon(':/icons/list-done.png')
        item.setIcon(icon)

    def add_message(self):
        text, _ = QInputDialog.getText(self, "item name", "item nnnname")
        if text:
            if text in self.messages:
                v = QMessageBox.warning(self, '', f'item {text} already exist, continue?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if QMessageBox.No == v:
                    return
                else:
                    for x in self.messages_list.findItems(text, Qt.Qt.MatchExactly):
                        self.messages_list.takeItem(self.messages_list.row(x))
                        break
            msg = Message(text, "", None)
            self.messages[text] = msg
            item = self.create_item(msg)
            self.messages_list.addItem(item)
            self.messages_list.setCurrentItem(item)

    def find_next(self):
        if self.find_msg_generator:
            try:
                next(self.find_msg_generator)
            except StopIteration:
                QMessageBox.information(self, '', 'messages list end reached')

    def find_msg_id_dialog(self):
        self.find_msg_generator = None
        text, _ = QInputDialog.getText(self, "find message", "find message by id")
        if text:
            def gen():
                for item in self.messages_list.findItems(text, Qt.Qt.MatchContains):
                    self.messages_list.setCurrentItem(item)
                    yield True

            self.find_msg_generator = gen()
            self.find_next()

    def find_msg_dialog(self):
        self.find_msg_generator = None
        text, _ = QInputDialog.getText(self, "find message", "find message by translated text")
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

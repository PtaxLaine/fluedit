import sys
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QMessageBox, QListWidgetItem
from PyQt5 import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QColor, QBrush
from .ui import editor
from .highlighter import Highlighter
from .playground import Playground
import fluent.syntax
import fluent.syntax.ast
import re


class Palette:
    DRAFT_COLOR = QColor(204, 136, 0)


def build(key, value):
    return key + " = " + value


class Message:
    def __init__(self, key, message, comment):
        self.key = key
        self.message = message
        self.draft = False
        self.original = None

        if comment:
            self.comment = self.parse_comment(comment)
        else:
            self.comment = comment

    def parse_comment(self, comment):
        eraser = []
        for x in re.finditer(r'^\s*fluedit:([a-zA-Z0-9]+)\s*$', comment, re.MULTILINE):
            value = x.group(1)
            if value == 'draft':
                self.draft = True
            span = x.span(0)
            eraser.append(span)
        eraser.sort(key=lambda x: x[0], reverse=True)
        for x in eraser:
            first = comment[:x[0]]
            last = comment[x[1]:].lstrip()
            comment = first + last
        return comment


class Editor(QWidget, editor.Ui_Editor):
    def __init__(self, filename):
        super().__init__()
        self.setupUi(self)

        self.playground = Playground()
        self.tab_playground_layout.addWidget(self.playground)

        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.is_draft_box.stateChanged.connect(self.on_draft_box_changed)

        self.create_message_button.clicked.connect(self.on_add_item)
        self.messages_list.currentRowChanged.connect(self.onCurrentRowChanged)

        self.textHighlighter = Highlighter(self.translited_message_edit)
        self.translited_message_edit.textChanged.connect(self.onTextChanged)

        self.messages = {}
        self.current_message = None

        self.filename = filename
        if filename:
            self.messages = self.load_file(filename)

        for x in self.messages.values():
            self.messages_list.addItem(self.create_item(x))
        self.messages_list.setCurrentRow(0)

    def load_file(self, filename):
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
                    QMessageBox.critical(self, '', 'file load error')
                elif isinstance(entity, fluent.syntax.ast.ResourceComment):
                    pass
                elif isinstance(entity, fluent.syntax.ast.GroupComment):
                    pass
        return messages

    def on_tab_changed(self, value):
        if value == 1:
            self.playground.translited_message_edit.setPlainText(self.messages[self.current_message].message)
        else:
            plain = self.playground.translited_message_edit.toPlainText()
            if plain != self.messages[self.current_message].message:
                v = QMessageBox.question(self, '', f'translated message was benn changed, apply changes?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if v == QMessageBox.Yes:
                    self.translited_message_edit.setPlainText(plain)

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
        with open(filename, 'w', encoding='UTF-8') as fs:
            for key, value in self.messages.items():
                fs.write(f'{key} = {value}\r\n')

    def on_draft_box_changed(self, value):
        msg = self.messages[self.current_message]
        msg.draft = value == Qt.Qt.Checked
        self.update_list_item(self.messages_list.currentItem(), msg)

    def onTextChanged(self):
        if self.current_message:
            plain = self.translited_message_edit.toPlainText()
            self.messages[self.current_message].message = plain

            syntax = fluent.syntax.FluentParser()
            entries = syntax.parse(build("f", plain))
            for enity in entries.body:
                if isinstance(enity, fluent.syntax.ast.Junk):
                    for ann in enity.annotations:
                        print(ann.message)
                        print(ann.args)
                        print(enity.span)
                        # self.textHighlighter.set_error((enity.span.start-4, enity.span.end-4), ann.message)

    def onCurrentRowChanged(self, row):
        item = self.messages_list.item(row).text()
        self.current_message = item
        msg = self.messages[item]
        self.translited_message_edit.setPlainText(msg.message)
        self.comments_edit.setPlainText(msg.comment if msg.comment else "")
        self.is_draft_box.setCheckState(Qt.Qt.Checked if msg.draft else Qt.Qt.Unchecked)

    def create_item(self, message) -> QListWidgetItem:
        item = QListWidgetItem(message.key)
        self.update_list_item(item, message)
        return item

    def update_list_item(self, item, message):
        brush = QBrush()
        if message.draft:
            brush = Palette.DRAFT_COLOR
        item.setBackground(brush)

    def on_add_item(self):
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

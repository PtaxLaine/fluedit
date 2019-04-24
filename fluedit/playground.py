import sys
import json
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QMessageBox
from PyQt5 import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSignal
from .ui import playground

from .highlighter import Highlighter
import re
import fluent.runtime
import fluent.syntax
import fluent.syntax.ast


class Playground(QWidget, playground.Ui_Playground):
    VARIABLE_DETECTOR = re.compile(r'\{\s*\$([a-zA-Z0-9_-]+)\s*\}', re.MULTILINE)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textHighlighter = Highlighter(self.translited_message_edit)
        self.variables = {}

    def clean(self):
        self.variables = {}
        self.variables_updated()

    def compile(self):
        msg = self.translited_message_edit.toPlainText()
        msg = f"msg = {msg}"

        if self.text_direction_box.currentIndex() == 0:
            char = '\u200E'
        else:
            char = '\u200F'

        try:
            syntax = fluent.syntax.FluentParser()
            entries = syntax.parse(msg)
            errors = ""
            for entity in entries.body:
                if isinstance(entity, fluent.syntax.ast.Junk):
                    for ann in entity.annotations:
                        errors += f'{ann.span}\n{ann.code} {ann.message}'
            if errors:
                self.console_edit.setPlainText(errors)
            else:
                variables = json.loads(self.variables_edit.toPlainText())
                self.variables = variables
                bundle = fluent.runtime.FluentBundle([self.language_box.currentText()])
                bundle.add_messages(msg)
                fmt, errors = bundle.format("msg", variables)
                self.output_edit.setPlainText(char + fmt)
                self.console_edit.setPlainText("\n".join(errors))
        except Exception as ex:
            self.console_edit.setPlainText(f'{type(ex).__name__}\n{ex}')

    def variables_updated(self):
        js = json.dumps(self.variables, indent=4, ensure_ascii=False)
        self.variables_edit.setPlainText(js)

    def update_variables(self):
        variables = set()
        msg = self.translited_message_edit.toPlainText()
        print(msg)
        for var in Playground.VARIABLE_DETECTOR.finditer(msg):
            variables.add(var.group(1))
        update = False
        for var in variables:
            if var not in self.variables:
                update = True
                self.variables[var] = None
        if update:
            self.variables_updated()

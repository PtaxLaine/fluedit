import json
import re
import time

import fluent.runtime
import fluent.syntax
import fluent.syntax.ast
from PyQt5.QtCore import QEvent, QTimer
from PyQt5.QtWidgets import QWidget

from .ui import playground


class Playground(QWidget, playground.Ui_Playground):
    VARIABLE_DETECTOR = re.compile(r'\$([a-zA-Z0-9_-]+)', re.MULTILINE)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.variables = {}
        self._last_variables_updated = 0

    def changeEvent(self, ev):
        super().changeEvent(ev)
        if ev.type() == QEvent.EnabledChange and self.isEnabled():
            self.compile()
            self.update_variables()

    def clean(self):
        self.variables = {}
        self.variables_updated()

    def compile(self):
        if not self.isEnabled():
            return
        if self.translited_message_edit.errors:
            self.console_edit.setPlainText("\n".join(
                map(lambda x: f'Line {x[0]} : {x[1]}', self.translited_message_edit.errors)
            ))
            return

        msg = self.translited_message_edit.toPlainText()
        msg = f"msg = {msg}"

        if self.text_direction_box.currentIndex() == 0:
            char = '\u200E'
        else:
            char = '\u200F'

        try:
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

    def _update_variables(self):
        variables = set()
        msg = self.translited_message_edit.toPlainText()
        for var in Playground.VARIABLE_DETECTOR.finditer(msg):
            variables.add(var.group(1))
        update = False
        for var in variables:
            if var not in self.variables:
                update = True
                self.variables[var] = 0
        if update:
            self.variables_updated()

    def update_variables(self):
        if not self.isEnabled():
            return

        def _tick():
            if time.monotonic() - self._last_variables_updated < 0.7:
                QTimer.singleShot(100, _tick)
            else:
                self._update_variables()
                self._last_variables_updated = 0

        if self._last_variables_updated == 0:
            self._last_variables_updated = time.monotonic()
            QTimer.singleShot(100, _tick)
        else:
            self._last_variables_updated = time.monotonic()

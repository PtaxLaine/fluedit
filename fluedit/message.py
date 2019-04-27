from __future__ import annotations

import base64
import re

import fluent.syntax
import fluent.syntax.ast

from .common import offset_to_line

from PyQt5.QtCore import pyqtSignal, QObject


# todo: msg_author, msg_date

class Message(QObject):
    changed = pyqtSignal(object)

    def __init__(self, key, message, comment=None):
        super().__init__()

        self.__key = key
        self.__message = message
        self.__draft = False
        self.__error = False
        self.__original = None
        self.__file = None

        if comment:
            self.__comment = self._parse_comment(comment)
        else:
            self.__comment = None

    @property
    def key(self):
        return self.__key

    def copy(self, new_key=None):
        msg = Message(self.__key, self.__message)
        msg.__draft = self.__draft
        msg.__error = self.__error
        msg.__original = self.__original
        msg.__file = self.__file
        msg.__comment = self.__comment
        if new_key:
            msg.__key = new_key
        return msg

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, o):
        self.__message = o
        self.changed.emit(self)

    @property
    def draft(self):
        return self.__draft

    @draft.setter
    def draft(self, o):
        self.__draft = o
        self.changed.emit(self)

    @property
    def error(self):
        return self.__error

    @error.setter
    def error(self, o):
        self.__error = o
        self.changed.emit(self)

    @property
    def original(self):
        return self.__original

    @original.setter
    def original(self, o):
        self.__original = o
        self.changed.emit(self)

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, o):
        self.__comment = o
        self.changed.emit(self)

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, o):
        self.__file = o

    def _parse_comment(self, comment):
        eraser = []
        for x in re.finditer(r'^[ \t]*fluedit:([a-zA-Z0-9]+)[ \t]*(.+)?$', comment, re.MULTILINE):
            value = x.group(1)
            if value == 'draft':
                self.draft = True
            elif value == 'original' and x.group(2):
                self.original = base64.b64decode(x.group(2)).decode()
            elif value == 'file' and x.group(2):
                f = x.group(2).rsplit(':', 1)
                self.file = (f[0], int(f[1]))
            span = x.span(0)
            eraser.append(span)
        eraser.sort(key=lambda x: x[0], reverse=True)
        for x in eraser:
            first = comment[:x[0]].rstrip()
            last = comment[x[1]:]
            comment = first + last
        return comment

    @property
    def is_translated(self):
        return self.message != self.original and not self.draft

    def to_string(self):
        res = ""
        if self.draft:
            res += "# fluedit:draft\n"
        if self.file:
            res += f"# fluedit:file {self.file[0]}:{self.file[1]}\n"
        if self.original:
            res += f"# fluedit:original {base64.b64encode(self.original.encode()).decode()}\n"
        if self.comment is not None and self.comment.strip():
            res += "\n".join(map(lambda x: '# ' + x, self.comment.split('\n')))
            res += "\n"

        res += self.key + ' = '
        if self.message.startswith(' ') and '\n' in self.message:
            res += '\n'
        res += self.message

        return res

    @staticmethod
    def build_file(messages: (Message,)) -> str:
        return "\n\n".join((x.to_string() for x in messages)) + "\n"

    @staticmethod
    def parse_file(file_data) -> ([Message], [str]):
        entries = fluent.syntax.FluentParser().parse(file_data)

        messages = []
        errors = []
        for entity in entries.body:
            if isinstance(entity, fluent.syntax.ast.Message):
                comment = entity.comment.content if entity.comment else None
                message = file_data[entity.value.span.start:entity.value.span.end]
                key = entity.id.name
                messages.append(Message(key, message, comment))
            elif isinstance(entity, fluent.syntax.ast.Junk):
                pos = offset_to_line(file_data, entity.span.start)
                errors.append(
                    "\n".join(map(lambda x: f'line: {pos[0]}   {x.code}: {x.message}',
                                  entity.annotations)))
            elif isinstance(entity, fluent.syntax.ast.ResourceComment):
                pass
            elif isinstance(entity, fluent.syntax.ast.GroupComment):
                pass
        return messages, errors

import re

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog

from .message import Message
from .ui.memoirs_search_dialog import Ui_MemoirsSearchDialog


class MemoirsSearchDialog(QDialog, Ui_MemoirsSearchDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setModal(True)
        self.setupUi(self)

    def on_text_changed(self):
        text = self.plainTextEdit.toPlainText()
        self.listWidget.clear()

        def completed(variants: (Memoirs.SearchResult,)):
            for v in variants:
                msg = v.msg
                self.listWidget.addItem(f'{msg.original}\n    {msg.message}')

        Memoirs.search(text, completed)


class Key:
    REGEX = re.compile(r"(\$[a-zA-Z0-9_]+)", re.MULTILINE)

    def __init__(self, original: str):
        self.value = self.convert(original)

    def diff(self, other: str) -> float:
        other = self.convert(other)
        diff = abs(len(self.value) - len(other))
        for (a, b) in zip(self.value, other):
            if a != b:
                diff += 1
        mlen = max(len(other), len(self.value))
        diff = (mlen - diff) / mlen
        return diff

    @staticmethod
    def convert(value: str):
        value = Key.REGEX.sub('', value)
        return " ".join(
            (x for x in (x.strip() for x in value.split()) if x)
        ).lower()

    def __hash__(self):
        return self.value.__hash__()

    def __eq__(self, other):
        return self.value == other.value


class Memoirs:
    __INSTANCE = None

    class SearchResult:
        def __init__(self, diff, msg: Message):
            self.diff = diff
            self.msg = msg

    @staticmethod
    def search_dialog(parent):
        Memoirs.instance()._search_dialog(parent)

    @staticmethod
    def append(msg: Message):
        Memoirs.instance()._append(msg)

    @staticmethod
    def search(msg: Message or str, callback: any):
        Memoirs.instance()._search(msg, callback)

    @staticmethod
    def instance():
        if not Memoirs.__INSTANCE:
            Memoirs.__INSTANCE = Memoirs()
        return Memoirs.__INSTANCE

    def __init__(self, fake_db=False):
        self.fake_db = fake_db
        if fake_db:
            self._db = {}
        else:
            db = QSettings().value("memoirs", {})
            self._db = {Key(x[0].original): x for x in (Message.parse_file(x)[0] for x in db)}

    def _search_dialog(self, parent):
        d = MemoirsSearchDialog(parent)
        d.show()

    def _append(self, msg: Message):
        key = Key(msg.original)

        cm = Key.convert(msg.message)
        for x in self._db.values():
            for alt in x:
                if cm == Key.convert(alt.message):
                    return

        variants = self._db.setdefault(key, [])
        variants.append(msg)

        self._commit()

    def _commit(self):
        if not self.fake_db:
            conf = QSettings()
            conf.setValue("memoirs",
                          [Message.build_file(msg) for key, msg in self._db.items()])
            conf.sync()

    def _search(self, msg: Message or str, callback: any or None):
        if isinstance(msg, Message):
            msg = msg.original

        result = []
        for key, value in self._db.items():
            for v in value:
                diff = key.diff(msg)
                if diff >= 0.7:
                    result.append((diff, v))
        if callback:
            callback([Memoirs.SearchResult(*x) for x in result])
        return result

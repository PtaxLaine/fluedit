import fluent.syntax
import fluent.syntax
import fluent.syntax.ast
import fluent.syntax.ast
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal, QSize, QRect
from PyQt5.QtGui import QTextCursor, QColor, QTextFormat, QPainter
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QWidget

from .common import offset_to_line
from .highlighter import Highlighter


class FluentMessageEditor(QTextEdit):
    error = pyqtSignal([bool])

    def __init__(self, parent):
        super().__init__(parent)
        self.textChanged.connect(self.on_text_changed)

        self.highlighter = Highlighter(self)
        self.lines = FluentMessageEditorLines(self)
        self.errors = []

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.lines.on_changed()

    def annotations_to_selection(self, offset, ann):
        selection = QTextEdit.ExtraSelection()

        start = ann.span.start - offset

        stop = ann.span.end - offset
        if start >= stop:
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

        selection.format.setBackground(QColor(255, 0, 0))
        selection.cursor = QTextCursor(self.document())
        selection.cursor.setPosition(max(0, start), QTextCursor.MoveAnchor)
        selection.cursor.setPosition(max(0, stop), QTextCursor.KeepAnchor)
        return selection

    def on_text_changed(self):
        plain = self.toPlainText()
        if not plain and self.isReadOnly():
            return
        parser = fluent.syntax.FluentParser()
        annex = "f = "
        entries = parser.parse(annex + plain)
        offset = len(annex)
        selections = []
        errors = []
        for entity in entries.body:
            if isinstance(entity, fluent.syntax.ast.Junk):
                for ann in entity.annotations:
                    errors.append((offset_to_line(plain, ann.span.start - offset)[0],
                                   ann.message))
                    selection = self.annotations_to_selection(offset, ann)
                    selections.append(selection)
        self.lines.set_errors(errors)
        self.setExtraSelections(selections)
        self.setToolTip("\n".join(map(lambda x: x[1], errors)))
        self.error.emit(True if errors else False)
        self.errors = errors


class FluentMessageEditorLines(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

        self.editor.verticalScrollBar().valueChanged.connect(self.on_scrolled)
        self.editor.document().blockCountChanged.connect(self.on_changed)
        self.scroll_top = 0

        self.errors = set()

    def set_errors(self, errs):
        self.errors = set()
        for x in errs:
            self.errors.add(x[0])
        self.repaint()

    def on_scrolled(self, v):
        self.scroll_top = v
        self.scroll(0, v)
        self.update(self.editor.rect())

    def on_changed(self):
        cr = self.editor.contentsRect()
        self.setGeometry(QRect(cr.left(), cr.top(), self.area_width(), cr.height()))
        self.editor.setViewportMargins(self.area_width(), 0, 0, 0)
        self.repaint()

    def area_width(self):
        digits = 1
        dmax = max(1, self.editor.document().blockCount())
        while dmax >= 10:
            dmax /= 10
            digits += 1

        space = 1.48 * (self.editor.fontMetrics().horizontalAdvance('9') * digits)
        return int(space)

    def sizeHint(self):
        return QSize(self.area_width(), 0)

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.fillRect(ev.rect(), Qt.Qt.lightGray)
        painter.setFont(self.editor.currentFont())

        block = self.editor.document().firstBlock()
        top = block.layout().boundingRect().translated(0, -self.scroll_top).top()
        top += 3  # TODO: magic number

        for i in range(1, self.editor.document().lineCount() + 1):
            painter.setPen(Qt.Qt.black if i not in self.errors else Qt.Qt.red)
            painter.drawText(0, top, self.width(), self.editor.fontMetrics().height(),
                             Qt.Qt.AlignCenter,
                             str(i))
            top += block.layout().boundingRect().height()
            block = block.next()

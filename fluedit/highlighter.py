from PyQt5.QtGui import QSyntaxHighlighter, QTextDocument, QTextCharFormat, QColor
from PyQt5 import Qt
import re


class HighlightingRule:
    def __init__(self, pattern, format):
        self.pattern = re.compile(pattern)
        self.format = format


class Format:
    def __init__(self):
        self.fmt = QTextCharFormat()

    def setForeground(self, x):
        self.fmt.setForeground(x)
        return self

    def build(self):
        return self.fmt


class Highlighter(QSyntaxHighlighter):
    def __init__(self, doc):
        super().__init__(doc)

        format = QTextCharFormat()
        format.setForeground(Qt.Qt.darkBlue)
        self.rules = []

        self.rules.append(HighlightingRule(r'\$[a-zA-Z0-9_-]+',
                                           Format(). \
                                           setForeground(QColor(102, 153, 153)). \
                                           build()))

        self.rules.append(HighlightingRule(r'\[[a-zA-Z0-9]+\]',
                                           Format(). \
                                           setForeground(QColor(255, 153, 51)). \
                                           build()))

        self.rules.append(HighlightingRule(r'\*\[[a-zA-Z0-9]+\]',
                                           Format(). \
                                           setForeground(QColor(255, 102, 102)). \
                                           build()))

        format = QTextCharFormat()
        format.setForeground(Qt.Qt.darkGreen);
        self.rules.append(HighlightingRule(
            "\".*\"",
            format
        ))

        self.errors = []

    def set_error(self, span, tooltip):
        self.errors.append((span, tooltip))

    def highlightBlock(self, text):
        for rule in self.rules:
            for match in rule.pattern.finditer(text):
                span = match.span()
                self.setFormat(span[0], span[1] - span[0], rule.format)

        for span, tooltip in self.errors:
            format = QTextCharFormat()
            format.setBackground(QColor(255, 0, 0))
            format.setToolTip(tooltip)
            self.setFormat(span[0], span[1] - span[0], format)

        self.setCurrentBlockState(0)

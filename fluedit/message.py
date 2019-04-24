import re


class Message:
    def __init__(self, key, message, comment, errors=None):
        self.key = key
        self.message = message
        self.draft = False
        self.errors = errors if errors else []
        self.original = "Stream status" if message == "Stream status" else None

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

    @property
    def is_translated(self):
        return self.message != self.original and not self.draft

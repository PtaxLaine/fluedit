import base64
import re


# todo: msg_author, msg_date

class Message:
    def __init__(self, key, message, comment=None, errors=None):
        self.key = key
        self.message = message
        self.draft = False
        self.errors = errors if errors else []
        self.original = None
        self.file = None

        if comment:
            self.comment = self._parse_comment(comment)
        else:
            self.comment = None

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

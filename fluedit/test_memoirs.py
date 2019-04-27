import unittest

from .message import Message
from .memoirs import Memoirs


def create_messae(msg, original):
    r = Message("", msg)
    r.original = original
    return r


class TestMemoirs(unittest.TestCase):
    def test_memoirs(self):
        mem = Memoirs(fake_db=True)
        mem._append(create_messae("немного $foo лет тому назад", "a some $foo time ago"))
        result = mem._search(create_messae("", "a some $bar time"), None)
        self.assertEqual([
            "немного $foo лет тому назад"
        ], [x[1].message for x in result])

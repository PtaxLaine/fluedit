import unittest

from .message import Message


class TestMessage(unittest.TestCase):
    def test_basic_constructor(self):
        msg = Message("13602927231834819367", "11706235081321450216")
        self.assertEqual(msg.key, "13602927231834819367")
        self.assertEqual(msg.message, "11706235081321450216")
        self.assertEqual(msg.draft, False)
        self.assertEqual(msg.original, None)
        self.assertEqual(msg.file, None)
        self.assertEqual(msg.comment, None)

    def test_draft_constructor(self):
        comments = "182140981\n   0687658970\n  1368504\n \t fluedit:draft\n\t3436615020316"
        msg = Message("13602927231834819367", "1170623\n50813\n2145\r\n0216", comments)
        self.assertEqual(msg.key, "13602927231834819367")
        self.assertEqual(msg.message, "1170623\n50813\n2145\r\n0216")
        self.assertEqual(msg.draft, True)
        self.assertEqual(msg.original, None)
        self.assertEqual(msg.file, None)
        self.assertEqual(msg.comment, "182140981\n   0687658970\n  1368504\n\t3436615020316")

    def test_original_constructor(self):
        comments = "182140981\n   0687658970\n  1368504\nfluedit:original MTM2ODUwNDM0MzY2MTUwMjAzMTY=\n3436615020316"
        msg = Message("13602927231834819367", "1170623\n50813\n2145\r\n0216", comments)
        self.assertEqual(msg.key, "13602927231834819367")
        self.assertEqual(msg.message, "1170623\n50813\n2145\r\n0216")
        self.assertEqual(msg.draft, False)
        self.assertEqual(msg.original, "13685043436615020316")
        self.assertEqual(msg.file, None)
        self.assertEqual(msg.comment, "182140981\n   0687658970\n  1368504\n3436615020316")

    def test_file_position_constructor(self):
        comments = "182140981\n   0687658970\n  1368504\nfluedit:file c:\\proj\\foo.bar:778\n3436615020316"
        msg = Message("13602927231834819367", "1170623\n50813\n2145\r\n0216", comments)
        self.assertEqual(msg.key, "13602927231834819367")
        self.assertEqual(msg.message, "1170623\n50813\n2145\r\n0216")
        self.assertEqual(msg.draft, False)
        self.assertEqual(msg.original, None)
        self.assertEqual(msg.file, ("c:\\proj\\foo.bar", 778))
        self.assertEqual(msg.comment, "182140981\n   0687658970\n  1368504\n3436615020316")

    def test_is_translated(self):
        # original == msg
        msg = Message("13602927231834819367",
                      "13685043436615020316",
                      "fluedit:original MTM2ODUwNDM0MzY2MTUwMjAzMTY=")
        self.assertFalse(msg.is_translated)

        # original != msg
        msg = Message("13602927231834819367",
                      "65173298876957731364",
                      "fluedit:original MTM2ODUwNDM0MzY2MTUwMjAzMTY=")
        self.assertTrue(msg.is_translated)

        # original == msg and is_draft
        msg = Message("13602927231834819367",
                      "13685043436615020316",
                      "fluedit:original MTM2ODUwNDM0MzY2MTUwMjAzMTY=\nfluedit:draft")
        self.assertFalse(msg.is_translated)

        # original != msg and is_draft
        msg = Message("13602927231834819367",
                      "65173298876957731364",
                      "fluedit:original MTM2ODUwNDM0MzY2MTUwMjAzMTY=\nfluedit:draft")
        self.assertFalse(msg.is_translated)

    def test_to_string_basic(self):
        msg = Message("13602927231834819367",
                      " 1170623\n 50813\n 2145\r\n 0216")
        self.assertEqual(msg.to_string(),
                         "13602927231834819367 = \n 1170623\n 50813\n 2145\r\n 0216")

    def test_to_string_with_comments(self):
        msg = Message("13602927231834819367",
                      "1170623\n 50813\n 2145\r\n 0216",
                      "14584842\n8148158230\n \t15")
        self.assertEqual(msg.to_string(),
                         "# 14584842\n# 8148158230\n#  \t15\n13602927231834819367 = 1170623\n 50813\n 2145\r\n 0216")

    def test_to_string_with_draft_and_comments(self):
        msg = Message("13602927231834819367",
                      "1170623\n 50813\n 2145\r\n 0216",
                      "14584842\nfluedit:draft")
        self.assertEqual(msg.to_string(),
                         "# fluedit:draft\n# 14584842\n13602927231834819367 = 1170623\n 50813\n 2145\r\n 0216")

    def test_to_string_with_original_and_comments(self):
        msg = Message("13602927231834819367", "1170623\n 50813\n 2145\r\n 0216",
                      "14584842\nfluedit:original MTM2ODUwNDM0MzY2MTUwMjAzMTY=")
        self.assertEqual(msg.to_string(),
                         "# fluedit:original MTM2ODUwNDM0MzY2MTUwMjAzMTY=\n# 14584842\n13602927231834819367 = 1170623\n 50813\n 2145\r\n 0216")

    def test_to_string_with_file_and_comments(self):
        msg = Message("13602927231834819367", "1170623\n 50813\n 2145\r\n 0216",
                      "14584842\nfluedit:file c:\\proj\\foo.bar:778")
        self.assertEqual(msg.to_string(),
                         "# fluedit:file c:\\proj\\foo.bar:778\n# 14584842\n13602927231834819367 = 1170623\n 50813\n 2145\r\n 0216")

    def test_file_parse(self):
        file = "foo=bar\n# comm\nbar=baz\nklkl"
        messages, errors = Message.parse_file(file)

        self.assertEqual(['line: 4   E0003: Expected token: "="'], errors)
        self.assertEqual(2, len(messages))

        self.assertEqual("foo", messages[0].key)
        self.assertEqual("bar", messages[0].message)
        self.assertEqual(False, messages[0].draft)
        self.assertEqual(None, messages[0].original)
        self.assertEqual(None, messages[0].file)
        self.assertEqual(None, messages[0].comment)

        self.assertEqual("bar", messages[1].key)
        self.assertEqual("baz", messages[1].message)
        self.assertEqual(False, messages[1].draft)
        self.assertEqual(None, messages[1].original)
        self.assertEqual(None, messages[1].file)
        self.assertEqual("comm", messages[1].comment)

    def test_build_file(self):
        messages = [
            Message("foo", "bar", "comico"),
            Message("bin", "bond", "fluedit:draft")
        ]
        result = Message.build_file(messages)
        self.assertEqual("# comico\nfoo = bar\n\n# fluedit:draft\nbin = bond\n",
                         result)

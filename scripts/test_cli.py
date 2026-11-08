import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "cli.py"
SPEC = importlib.util.spec_from_file_location("cardlink_cli", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CardLinkCliTests(unittest.TestCase):
    def test_build_reference(self):
        self.assertEqual(MODULE.build("abc123", "目录"), "[Card#ID/abc123#目录]")

    def test_rejects_empty_label(self):
        with self.assertRaises(ValueError):
            MODULE.build("abc123", " ")

    def test_rejects_bracket_label(self):
        with self.assertRaises(ValueError):
            MODULE.build("abc123", "a]b")

    def test_check_roundtrip(self):
        value = MODULE.build("abc123", "第一章")
        parsed = MODULE.check(value)
        self.assertEqual(parsed["root_id"], "abc123")
        self.assertEqual(parsed["label"], "第一章")

    def test_rejects_web_url(self):
        with self.assertRaises(ValueError):
            MODULE.check("https://www.markji.com/deck/editor/x?cardId=y")


if __name__ == "__main__":
    unittest.main()

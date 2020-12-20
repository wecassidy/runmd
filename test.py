import unittest

from runmd import *


class TestCommandBuilder(unittest.TestCase):
    def test_append(self):
        self.assertEqual(build_command("test", "name"), "test name")

    def test_insert(self):
        self.assertEqual(build_command("test %s t", "name"), "test name t")

    def test_multi_insert(self):
        self.assertEqual(
            build_command("cmd %s foo %s", "/tmp/hi"), "cmd /tmp/hi foo /tmp/hi"
        )

    def test_ignore(self):
        self.assertEqual(build_command("%s %d %%s %", "test %s"), "test %s %d %s %")

    def test_lots_escape(self):
        self.assertEqual(build_command("%%%s", "name"), "%name")


if __name__ == "__main__":
    unittest.main()

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


if __name__ == "__main__":
    unittest.main()

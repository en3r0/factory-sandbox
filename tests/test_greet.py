import subprocess
import sys
import unittest

from greet import greet


class GreetTest(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Ada"), "Hello, Ada!")

    def test_greet_shout(self):
        self.assertEqual(greet("Ada", shout=True), "HELLO, ADA!")


class TestGreetCLI(unittest.TestCase):
    """Test the CLI via subprocess."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = __file__.rsplit("/", 1)[0] + "/.."

    def _run(self, *args):
        result = subprocess.run(
            [sys.executable, "greet.py", *args],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip(), result.returncode

    def test_no_args(self):
        stdout, rc = self._run()
        self.assertEqual(stdout, "Hello, world!")
        self.assertEqual(rc, 0)

    def test_name_arg(self):
        stdout, rc = self._run("Ada")
        self.assertEqual(stdout, "Hello, Ada!")
        self.assertEqual(rc, 0)

    def test_shout_only(self):
        stdout, rc = self._run("--shout")
        self.assertEqual(stdout, "HELLO, WORLD!")
        self.assertEqual(rc, 0)

    def test_name_then_shout(self):
        stdout, rc = self._run("Ada", "--shout")
        self.assertEqual(stdout, "HELLO, ADA!")
        self.assertEqual(rc, 0)

    def test_shout_then_name(self):
        stdout, rc = self._run("--shout", "Ada")
        self.assertEqual(stdout, "HELLO, ADA!")
        self.assertEqual(rc, 0)

    def test_help(self):
        stdout, rc = self._run("--help")
        self.assertEqual(rc, 0)
        self.assertIn("--shout", stdout)


if __name__ == "__main__":
    unittest.main()
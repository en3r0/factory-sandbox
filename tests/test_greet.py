import unittest

from greet import greet


class GreetTest(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Ada"), "Hello, Ada!")

    def test_greet_shout(self):
        self.assertEqual(greet("Ada", shout=True), "HELLO, ADA!")


if __name__ == "__main__":
    unittest.main()

import random
import unittest


class TestFlaky(unittest.TestCase):

    def test_flaky(self):
        self.assertTrue(random.random() < 0.20)

if __name__ == "__main__":
    unittest.main()
import random
import time
import unittest


class TestFlaky(unittest.TestCase):

    def test_flaky_seventy(self):
        time.sleep(random.randint(0, 7))
        self.assertTrue(random.random() < 0.70)

    def test_flaky_eighty(self):
        time.sleep(random.randint(0, 8))
        self.assertTrue(random.random() < 0.80)

    def test_flaky_ninety(self):
        time.sleep(random.randint(0, 9))
        self.assertTrue(random.random() < 0.90)


if __name__ == "__main__":
    unittest.main()
import random
import time
import unittest


class TestFlaky(unittest.TestCase):

    def test_flaky(self):
        time.sleep(2)
        self.assertTrue(random.random() < 0.20)

    def test_flaky_high_chance(self):
        time.sleep(8)
        self.assertTrue(random.random() < 0.80)


if __name__ == "__main__":
    unittest.main()

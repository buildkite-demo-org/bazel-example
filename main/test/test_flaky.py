import random
import time
import unittest


class TestFlaky(unittest.TestCase):

    def test_flaky(self):
        time.sleep(5)
        self.assertTrue(random.random() < 0.20)

if __name__ == "__main__":
    unittest.main()
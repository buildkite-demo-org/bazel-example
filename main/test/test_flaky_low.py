import random
import time
import unittest


class TestFlaky(unittest.TestCase):

    def test_flaky_ten(self):
        time.sleep(random.randint(0, 1))
        self.assertTrue(random.random() < 0.10)

    def test_flaky_twenty(self):
        time.sleep(random.randint(0, 2))
        self.assertTrue(random.random() < 0.20)

    def test_flaky_thirty(self):
        time.sleep(random.randint(0, 3))
        self.assertTrue(random.random() < 0.30)

if __name__ == "__main__":
    unittest.main()

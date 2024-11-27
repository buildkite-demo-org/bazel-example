import random
import time
import unittest


class TestFlaky(unittest.TestCase):



    def test_flaky_forty(self):
        time.sleep(random.randint(0, 4))
        self.assertTrue(random.random() < 0.40)

    def test_flaky_fifty(self):
        time.sleep(random.randint(0, 5))
        self.assertTrue(random.random() < 0.50)

    def test_flaky_sixty(self):
        time.sleep(random.randint(0, 6))
        self.assertTrue(random.random() < 0.60)


if __name__ == "__main__":
    unittest.main()
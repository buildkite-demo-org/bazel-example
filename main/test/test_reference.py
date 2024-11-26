import time
import unittest


class TestReference(unittest.TestCase):

    def test_always_true(self):
        time.sleep(7)
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
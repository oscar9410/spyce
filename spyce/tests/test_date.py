import unittest
import random

import date


class TestDate(unittest.TestCase):
    def test_human_time(self):
        t = random.uniform(0, 1e11)
        s = date.to_human_time(t)
        self.assertAlmostEqual(date.from_human_time(s), t, places=6)

    def test_human_date(self):
        t = random.uniform(0, 1e11)
        s = date.to_human_date(t)
        self.assertAlmostEqual(date.from_human_date(s), t, places=6)

    def test_kerbal_time(self):
        t = random.uniform(0, 1e11)
        s = date.to_kerbal_time(t)
        self.assertAlmostEqual(date.from_kerbal_time(s), t, places=1)

    def test_kerbal_date(self):
        t = random.uniform(0, 1e11)
        s = date.to_kerbal_date(t)
        self.assertAlmostEqual(date.from_kerbal_date(s), t, places=1)


if __name__ == '__main__':
    unittest.main()
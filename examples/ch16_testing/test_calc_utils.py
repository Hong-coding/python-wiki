# 실행: ch16_testing 폴더에서  python -m unittest -v
import unittest

from calc_utils import average, normalize_email


class AverageTest(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(average([1, 2, 3]), 2)

    def test_float(self):
        self.assertAlmostEqual(average([0.1, 0.2]), 0.15)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            average([])


class NormalizeEmailTest(unittest.TestCase):
    def test_strip_and_lower(self):
        self.assertEqual(normalize_email("  Kim@Example.COM "), "kim@example.com")

    def test_invalid(self):
        for bad in ["", "abc", "   "]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    normalize_email(bad)


if __name__ == "__main__":
    unittest.main()

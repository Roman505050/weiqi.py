import unittest
from parameterized import parameterized  # type: ignore[import-untyped]

from weiqi.bot import RandomBot


class MyTestCase(unittest.TestCase):
    @parameterized.expand(
        [
            ([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], 0.75),
            ([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 1]], 0.8125),
            ([[0, 0, 0, 0], [1, 0, 1, 1], [1, 1, 0, 1], [1, 0, 0, 2]], 0.5),
            ([[0, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 3]], 0.875),
            ([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 4]], 1.0),
            ([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 0.0),
        ]
    )
    def test_calc_field_boars(self, matrix: list[list[int]], expected: float):
        self.assertEqual(RandomBot._calc_field_boars(matrix), expected)


if __name__ == "__main__":
    unittest.main()

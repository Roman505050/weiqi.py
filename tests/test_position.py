import unittest
from weiqi.position import Position


class TestPlayer(unittest.TestCase):
    def test_addition(self):
        a = Position(1, 2)
        b = Position(3, 4)

        self.assertEqual(a + b, Position(4, 6))


if __name__ == "__main__":
    unittest.main()

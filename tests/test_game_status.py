import unittest

from weiqi.utils.enums import Winner
from weiqi.utils.game_status import GameStatus


class TestGameStatus(unittest.TestCase):
    def test_missing_winner(self):
        with self.assertRaises(ValueError):
            GameStatus(is_over=True, winner=None)

    def test_provided_one_score(self):
        with self.assertRaises(ValueError):
            GameStatus(is_over=True, winner=Winner.WHITE, black_score=1)

        game_status_not_over = GameStatus(is_over=False, winner=None)
        with self.assertRaises(ValueError):
            game_status_not_over.end_game(Winner.WHITE, 1, None)


if __name__ == "__main__":
    unittest.main()

import unittest

from weiqi.core.game import WeiqiGame
from weiqi.players.player import Player
from weiqi.core.position import Position
from weiqi.core.figure import Stone
from weiqi.core.board import Board


class TestPlayer(unittest.TestCase):
    @staticmethod
    def get_game():
        board = Board.generate_empty_board(9)
        player_black = Player(user="Alice", figure=Stone.BLACK)
        player_white = Player(user="Bob", figure=Stone.WHITE)
        return WeiqiGame(
            board=board, player_black=player_black, player_white=player_white
        )

    def test_makes_move_correctly(self):
        game = self.get_game()
        player = game.get_current_player()

        player.make_move(game, Position(0, 0))
        self.assertEqual(game.board.figures[Position(0, 0)], Stone.BLACK)

        with self.assertRaises(ValueError):
            player.make_move(game, Position(0, 2))

    def test_raises_error_on_invalid_move(self):
        game = self.get_game()
        player = game.get_current_player()

        with self.assertRaises(ValueError):
            player.make_move(game, Position(10, 10))


if __name__ == "__main__":
    unittest.main()

import unittest
from weiqi.player import Player
from weiqi.position import Position
from weiqi.figure import Stone
from weiqi.board import Board


class TestPlayer(unittest.TestCase):
    def test_makes_move_correctly(self):
        board = Board.generate_empty_board(9)
        player = Player(user="Alice", color=Stone.BLACK)
        position = Position(0, 0)
        player.make_move(position, board)
        self.assertEqual(board.figures[position], Stone.BLACK)

    def test_raises_error_on_invalid_move(self):
        board = Board.generate_empty_board(9)
        player = Player(user="Alice", color=Stone.BLACK)
        position = Position(10, 10)
        with self.assertRaises(ValueError):
            player.make_move(position, board)


if __name__ == "__main__":
    unittest.main()

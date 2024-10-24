import unittest
from weiqi.board import Board
from weiqi.position import Position
from weiqi.figure import Stone
from weiqi.move import Move


class TestBoard(unittest.TestCase):
    def test_generates_empty_board_correctly(self):
        board = Board.generate_empty_board(9)
        self.assertEqual(len(board.figures), 81)
        self.assertTrue(all(stone is None for stone in board.figures.values()))

    def test_from_state_creates_correct_board(self):
        state = [
            [1, -1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        board = Board(state)
        self.assertEqual(board.figures[Position(0, 0)], Stone.BLACK)
        self.assertEqual(board.figures[Position(0, 1)], Stone.WHITE)
        self.assertIsNone(board.figures[Position(1, 0)])

    def test_state_representation_is_correct(self):
        board = Board.generate_empty_board(5)
        board.place_figure(Move(Position(0, 0), Stone.BLACK))
        board.place_figure(Move(Position(0, 1), Stone.WHITE))
        expected_state = [
            [1, -1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.assertEqual(board.state_as_matrix, expected_state)

    def test_position_in_bounds_checks_correctly(self):
        board = Board.generate_empty_board(9)
        self.assertTrue(board.position_in_bounds(Position(0, 0)))
        self.assertFalse(board.position_in_bounds(Position(9, 9)))

    def test_place_figure_places_correctly(self):
        board = Board.generate_empty_board(9)
        board.place_figure(Move(Position(0, 0), Stone.BLACK))
        self.assertEqual(board.figures[Position(0, 0)], Stone.BLACK)

    def test_place_figure_raises_on_occupied_position(self):
        board = Board.generate_empty_board(9)
        board.place_figure(Move(Position(0, 0), Stone.BLACK))
        with self.assertRaises(ValueError):
            board.place_figure(Move(Position(0, 0), Stone.WHITE))

    def test_place_figure_raises_on_out_of_bounds(self):
        board = Board.generate_empty_board(9)
        with self.assertRaises(ValueError):
            board.place_figure(Move(Position(9, 9), Stone.BLACK))

    def test_place_figure_removes_captured_group(self):
        state = [
            [-1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        board = Board(state)
        self.assertIsNone(board.figures[Position(0, 0)])

    def test_place_figure_removes_double_captured_group(self):
        state = [
            [-1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1],
            [-1, 1, 1, 1, -1],
            [-1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0],
        ]
        board = Board(state)
        expected_state = [
            [-1, 0, 0, 0, -1],
            [-1, 0, 0, 0, -1],
            [-1, 0, 0, 0, -1],
            [-1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0],
        ]
        self.assertEqual(board.state_as_matrix, expected_state)

    def test_place_figure_allows_suicide_if_enabled(self):
        board = Board.generate_empty_board(9)
        board.place_figure(Move(Position(0, 0), Stone.BLACK))
        board.place_figure(Move(Position(0, 1), Stone.WHITE))
        board.place_figure(Move(Position(1, 0), Stone.WHITE))
        board.place_figure(Move(Position(1, 1), Stone.WHITE))
        self.assertIsNone(board.figures[Position(0, 0)])

    def test_not_square_board(self):
        figures = {
            Position(0, 0): None,
            Position(1, 0): None,
            Position(0, 1): None,
            Position(1, 1): None,
            Position(0, 2): None,
            Position(1, 2): None,
            Position(0, 3): None,
            Position(1, 3): None,
            Position(0, 4): None,
            Position(1, 4): None,
            Position(2, 0): None,
            Position(3, 0): None,
            Position(2, 1): None,
            Position(3, 1): None,
            Position(2, 2): None,
            Position(3, 2): None,
            Position(2, 3): None,
            Position(3, 3): None,
            Position(2, 4): None,
            Position(3, 4): None,
            Position(4, 0): None,
            Position(4, 1): None,
            Position(4, 2): None,
            Position(4, 3): None,
            Position(4, 4): None,
        }
        board = Board(figures)
        self.assertEqual(board.size, 5)

        figures[Position(5, 5)] = None

        with self.assertRaises(ValueError):
            Board(figures)

        state_as_matrix = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        board = Board(state_as_matrix)
        self.assertEqual(board.size, 5)

        state_as_matrix.append([0, 0, 0, 0, 0])
        with self.assertRaises(ValueError):
            Board(state_as_matrix)

        state_as_string = "...../...../...../...../....."
        board = Board(state_as_string)
        self.assertEqual(board.size, 5)

        state_as_string += "."
        with self.assertRaises(ValueError):
            Board(state_as_string)


if __name__ == "__main__":
    unittest.main()

import unittest
from weiqi.board import Board
from weiqi.position import Position
from weiqi.figure import Stone


class TestBoard(unittest.TestCase):
    def test_generates_empty_board_correctly(self):
        board = Board.generate_empty_board(9)
        self.assertEqual(len(board.figures), 81)
        self.assertTrue(all(stone is None for stone in board.figures.values()))

    def test_from_state_creates_correct_board(self):
        state = [
            [1, 0, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
        ]
        board = Board.from_state(state)
        self.assertEqual(board.figures[Position(0, 0)], Stone.BLACK)
        self.assertEqual(board.figures[Position(0, 1)], Stone.WHITE)
        self.assertIsNone(board.figures[Position(1, 0)])

    def test_state_representation_is_correct(self):
        board = Board.generate_empty_board(5)
        board.place_figure(Position(0, 0), Stone.BLACK)
        board.place_figure(Position(0, 1), Stone.WHITE)
        expected_state = [
            [1, 0, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
        ]
        self.assertEqual(board.state, expected_state)

    def test_position_in_bounds_checks_correctly(self):
        board = Board.generate_empty_board(9)
        self.assertTrue(board.position_in_bounds(Position(0, 0)))
        self.assertFalse(board.position_in_bounds(Position(9, 9)))

    def test_place_figure_places_correctly(self):
        board = Board.generate_empty_board(9)
        board.place_figure(Position(0, 0), Stone.BLACK)
        self.assertEqual(board.figures[Position(0, 0)], Stone.BLACK)

    def test_place_figure_raises_on_occupied_position(self):
        board = Board.generate_empty_board(9)
        board.place_figure(Position(0, 0), Stone.BLACK)
        with self.assertRaises(ValueError):
            board.place_figure(Position(0, 0), Stone.WHITE)

    def test_place_figure_raises_on_out_of_bounds(self):
        board = Board.generate_empty_board(9)
        with self.assertRaises(ValueError):
            board.place_figure(Position(9, 9), Stone.BLACK)

    def test_place_figure_removes_captured_group(self):
        state = [
            [0, 1, -1, -1, -1],
            [1, 1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
        ]
        board = Board.from_state(state)
        self.assertIsNone(board.figures[Position(0, 0)])

    def test_place_figure_removes_double_captured_group(self):
        state = [
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1],
        ]
        board = Board.from_state(state)
        expected_state = [
            [0, -1, -1, -1, 0],
            [0, -1, -1, -1, 0],
            [0, -1, -1, -1, 0],
            [0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1],
        ]
        self.assertEqual(board.state, expected_state)

    def test_place_figure_allows_suicide_if_enabled(self):
        board = Board.generate_empty_board(9)
        board.place_figure(Position(0, 0), Stone.BLACK)
        board.place_figure(Position(0, 1), Stone.WHITE)
        board.place_figure(Position(1, 0), Stone.WHITE)
        board.place_figure(Position(1, 1), Stone.WHITE)
        self.assertIsNone(board.figures[Position(0, 0)])


if __name__ == "__main__":
    unittest.main()

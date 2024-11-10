from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import random

from weiqi.core.figure import Stone
from weiqi.core.position import Position
from weiqi.core.move import Move
from weiqi.core.board import Board

if TYPE_CHECKING:
    from weiqi.core.game import WeiqiGame


class BaseBot(ABC):
    def __init__(self, figure: Stone):
        self._figure = figure

    @property
    def figure(self) -> Stone:
        return self._figure

    @abstractmethod
    def make_move(self, game: "WeiqiGame") -> Move: ...

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseBot):
            return NotImplemented
        return self.figure == other.figure and type(self) is type(other)


class RandomBot(BaseBot):
    @staticmethod
    def _calc_field_board(matrix: list[list[int]]) -> float:
        """Calculates the field board in percentage from the matrix."""
        count_non_zero = sum(1 for row in matrix for x in row if x != 0)
        total_elements = len(matrix) * len(matrix[0]) if matrix else 0
        return count_non_zero / total_elements if total_elements > 0 else 0.0

    @staticmethod
    def _should_pass_after_opponent_pass(last_move: Move | None) -> bool:
        return (
            last_move is not None
            and last_move.position is None
            and random.random() < 0.4
        )

    @staticmethod
    def _get_random_position(size: int) -> Position:
        x_rand = random.randint(0, size - 1)
        y_rand = random.randint(0, size - 1)
        return Position(x_rand, y_rand)

    def make_move(self, game: "WeiqiGame") -> Move:
        board = game.board
        last_move = game.move_history.last_move

        if self._should_pass_after_opponent_pass(last_move):
            return self._make_pass_move(game)

        if self._should_pass_on_high_occupancy(board):
            return self._make_pass_move(game)

        return self._make_random_valid_move(game, board)

    def _should_pass_on_high_occupancy(self, board: Board) -> bool:
        state_as_matrix = board.state_as_matrix
        fielded_board = self._calc_field_board(state_as_matrix)
        return 0.8 <= fielded_board <= 1.0 and random.random() < 0.4

    def _make_pass_move(self, game: "WeiqiGame") -> Move:
        """Makes a pass move."""
        move = Move(position=None, figure=self.figure)
        game.make_move(self, move)
        return move

    def _make_random_valid_move(
        self, game: "WeiqiGame", board: Board
    ) -> Move:
        """Makes a random valid move."""
        max_attempts = 15
        for attempt in range(max_attempts):
            position = self._get_random_position(board.size)
            move = Move(position=position, figure=self.figure)
            if board.figures[position] is None:
                try:
                    game.make_move(self, move)
                    return move
                except ValueError:
                    continue
        # If no valid move was found, pass.
        return self._make_pass_move(game)

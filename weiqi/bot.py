from abc import ABC, abstractmethod
import random

from weiqi.board import Board
from weiqi.figure import Stone
from weiqi.position import Position
from weiqi.move import Move
import copy


class BaseBot(ABC):
    def __init__(self, figure: Stone):
        self._figure = figure

    @property
    def figure(self) -> Stone:
        return self._figure

    @abstractmethod
    def make_move(self, board: Board): ...


class RandomBot(BaseBot):
    def make_move(self, board: Board):
        count = 0
        while True:
            x_rand = random.randint(0, board.size - 1)
            y_rand = random.randint(0, board.size - 1)
            position = Position(x_rand, y_rand)
            move = Move(position, self.figure)
            if board.figures[position] is None:
                try:
                    board.place_figure(move)
                except ValueError:
                    count += 1
                    if count < 15:
                        continue
                    else:
                        raise ValueError("RandomBot can't find a valid move")
                    continue
                break


class SmartBot(BaseBot):
    def make_move(self, board: Board) -> None:
        valid_moves = self._get_valid_moves(board)
        if not valid_moves:
            return None  # Pass if no valid moves available

        simulations_per_move = 100
        move_scores: dict[Move, int] = {move: 0 for move in valid_moves}

        for move in valid_moves:
            for _ in range(simulations_per_move):
                simulated_board = copy.deepcopy(board)
                simulated_board.place_figure(move)
                outcome = self._simulate_random_playout(simulated_board)
                move_scores[move] += outcome
                print(move, outcome)

        best_move: Move = max(move_scores, key=lambda move: move_scores[move])
        board.place_figure(best_move)

    def _get_valid_moves(self, board: Board) -> list[Move]:
        valid_moves = []
        for position in board._figures.keys():
            if board.figures[position] is None:
                move = Move(position, self.figure)
                board_copy = copy.deepcopy(board)
                if self._is_legal_move(board_copy, move):
                    valid_moves.append(move)
        return valid_moves

    def _is_legal_move(self, board: Board, move: Move) -> bool:
        try:
            board.place_figure(move)
            return True
        except ValueError:
            return False

    def _simulate_random_playout(self, board: Board) -> int:
        # Simulate a random game from the current board position
        # Returns +1 if the bot's color wins, -1 if it loses
        current_color = self.figure
        for _ in range(50):  # Limit playout depth
            valid_moves = self._get_valid_moves(board)
            if not valid_moves:
                break
            random_move = random.choice(valid_moves)
            board.place_figure(random_move)
            current_color = (
                Stone.BLACK if current_color == Stone.WHITE else Stone.WHITE
            )

        return self._evaluate_board(board)

    # TODO:rework this method(wron alhorithm)
    def _evaluate_board(self, board: Board) -> int:
        # Example evaluation: check the board state for bot's advantage
        bot_score = sum(
            1 for stone in board.figures.values() if stone == self.figure
        )
        opponent_score = sum(
            1
            for stone in board.figures.values()
            if stone != self.figure and stone is not None
        )
        return 1 if bot_score > opponent_score else -1

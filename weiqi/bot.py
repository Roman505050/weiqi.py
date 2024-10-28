from abc import ABC, abstractmethod
import random

from weiqi.board import Board
from weiqi.figure import Stone
from weiqi.position import Position
from weiqi.move import Move


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
                break

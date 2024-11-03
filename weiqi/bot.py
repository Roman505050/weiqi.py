from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import random

from weiqi.figure import Stone
from weiqi.position import Position
from weiqi.move import Move

if TYPE_CHECKING:
    from weiqi.game import WeiqiGame
    from weiqi.player import TUser


class BaseBot(ABC):
    def __init__(self, figure: Stone):
        self._figure = figure

    @property
    def figure(self) -> Stone:
        return self._figure

    @abstractmethod
    def make_move(self, game: "WeiqiGame[TUser]") -> Move: ...

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseBot):
            return NotImplemented
        return self.figure == other.figure and type(self) is type(other)


class RandomBot(BaseBot):
    def make_move(self, game: "WeiqiGame[TUser]") -> Move:
        board = game.board

        count = 0
        while True:
            x_rand = random.randint(0, board.size - 1)
            y_rand = random.randint(0, board.size - 1)
            position = Position(x_rand, y_rand)
            move = Move(position=position, figure=self.figure)
            if board.figures[position] is None:
                try:
                    game.make_move(self, move)
                except ValueError:
                    count += 1
                    if count < 15:
                        continue
                    else:
                        raise ValueError("RandomBot can't find a valid move")
                break
        return move

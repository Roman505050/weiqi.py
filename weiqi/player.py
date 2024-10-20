from typing import Generic, TypeVar

from weiqi.board import BaseBoard
from weiqi.figure import Stone
from weiqi.position import Position

TUser = TypeVar("TUser")


class Player(Generic[TUser]):
    def __init__(self, user: TUser, color: Stone):
        self._user = user
        self._color = color

    @property
    def user(self) -> TUser:
        return self._user

    @property
    def color(self) -> Stone:
        return self._color

    def make_move(self, position: Position, board: BaseBoard):
        board.place_figure(position, self.color)

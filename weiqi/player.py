from typing import Generic, TypeVar

from weiqi.board import Board
from weiqi.figure import Stone
from weiqi.position import Position
from weiqi.move import Move

TUser = TypeVar("TUser")


class Player(Generic[TUser]):
    def __init__(self, user: TUser, figure: Stone):
        self._user = user
        self._figure = figure

    @property
    def user(self) -> TUser:
        return self._user

    @property
    def figure(self) -> Stone:
        return self._figure

    def make_move(self, board: Board, position: Position) -> Move:
        move = Move(position=position, figure=self.figure)
        board.place_figure(move)
        return move

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.user == other.user and self.figure == other.figure

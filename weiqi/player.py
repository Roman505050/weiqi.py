from typing import Generic, TypeVar, TYPE_CHECKING

from weiqi.figure import Stone
from weiqi.position import Position
from weiqi.move import Move

if TYPE_CHECKING:
    from weiqi.game import WeiqiGame

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

    def make_move(self, game: "WeiqiGame[TUser]", position: Position) -> None:
        move = Move(position=position, figure=self.figure)
        game.make_move(self, move)

    def resign(self, game: "WeiqiGame[TUser]") -> None:
        game.resign(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.user == other.user and self.figure == other.figure

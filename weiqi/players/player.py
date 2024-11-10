from typing import TYPE_CHECKING

from weiqi.core.figure import Stone
from weiqi.core.position import Position
from weiqi.core.move import Move

if TYPE_CHECKING:
    from weiqi.core.game import WeiqiGame


class Player:
    def __init__(self, figure: Stone):
        self._figure = figure

    @property
    def figure(self) -> Stone:
        return self._figure

    def make_move(
        self, game: "WeiqiGame", position: Position | None
    ) -> None:
        move = Move(position=position, figure=self.figure)
        game.make_move(self, move)

    def resign(self, game: "WeiqiGame") -> None:
        game.resign(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.figure == other.figure

from weiqi.core.figure import Stone
from weiqi.core.position import Position


class Group:
    def __init__(
        self, positions: set[Position], liberties: set[Position], figure: Stone
    ):
        self.positions = positions
        self.liberties = liberties
        self.figure = figure

    def __hash__(self):
        return hash(
            (frozenset(self.positions), frozenset(self.liberties), self.figure)
        )

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False
        return (
            frozenset(self.positions) == frozenset(other.positions)
            and frozenset(self.liberties) == frozenset(other.liberties)
            and self.figure == other.figure
        )

from weiqi.figure import Stone
from weiqi.position import Position


class Group:
    def __init__(
        self, positions: set[Position], liberties: set[Position], figure: Stone
    ):
        self.positions = positions
        self.liberties = liberties
        self.figure = figure

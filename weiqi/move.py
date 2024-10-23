from dataclasses import dataclass

from weiqi.position import Position
from weiqi.figure import Stone


@dataclass(frozen=True)
class Move:
    position: Position
    figure: Stone

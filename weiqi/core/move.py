from bisect import insort
from dataclasses import dataclass, field
import datetime

from weiqi.core.position import Position
from weiqi.core.figure import Stone


@dataclass(frozen=True)
class Move:
    position: Position | None
    figure: Stone
    timestamp: datetime.datetime = field(init=False)

    def __post_init__(self):
        utc_tz = datetime.timezone.utc
        object.__setattr__(self, "timestamp", datetime.datetime.now(utc_tz))


class MoveHistory:
    def __init__(self, history: list[Move] | None = None):
        self._history = history or []
        self._history.sort(key=lambda m: m.timestamp)

    def add_move(self, move: Move):
        insort(self._history, move, key=lambda m: m.timestamp)

    @property
    def last_move(self) -> Move | None:
        if self._history:
            return self._history[-1]
        return None

    def get_all_moves(self) -> list[Move]:
        return self._history

    def __iter__(self):
        return iter(self._history)

    def __len__(self):
        return len(self._history)

    def __getitem__(self, item):
        return self._history[item]

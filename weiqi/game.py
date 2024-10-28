from typing import Generic

from weiqi.board import Board
from weiqi.figure import Stone
from weiqi.player import Player, TUser
from weiqi.bot import BaseBot
from weiqi.position import Position


class WeiqiGame(Generic[TUser]):
    def __init__(
        self,
        board: Board,
        player_black: Player[TUser] | BaseBot,
        player_white: Player[TUser] | BaseBot,
        turn: Stone | None = None,
    ):
        self._board = board
        self._players = [player_black, player_white]
        self._turn = turn or Stone.BLACK

    @property
    def board(self) -> Board:
        return self._board

    @property
    def players(self) -> list[Player[TUser] | BaseBot]:
        return self._players

    @property
    def turn(self) -> Stone:
        return self._turn

    def _validate_players(self):
        if not all(
            isinstance(player, (Player, BaseBot)) for player in self._players
        ):
            raise ValueError("Invalid player type.")
        if all(isinstance(player, BaseBot) for player in self._players):
            raise ValueError("At least one player must be human.")
        if not all(
            player.figure in (Stone.BLACK, Stone.WHITE)
            for player in self._players
        ):
            raise ValueError("Invalid player color.")
        if len(set(player.figure for player in self._players)) != 2:
            raise ValueError("Players must have different colors.")

    def get_current_player(self) -> Player[TUser] | BaseBot:
        return next(
            player for player in self._players if player.figure == self._turn
        )

    @property
    def score(self) -> dict[Stone, int]:
        black_score = 0
        white_score = 0
        for figure in self._board.figures.values():
            if figure is not None:
                if figure == Stone.BLACK:
                    black_score += 1
                else:
                    white_score += 1
        return {Stone.BLACK: black_score, Stone.WHITE: white_score}

    def make_move(self, x: int | None = None, y: int | None = None):
        player = self.get_current_player()
        if isinstance(player, Player):
            if x is None or y is None:
                raise ValueError("Position is required.")
            position = Position(x, y)
            player.make_move(self._board, position)
        else:
            if x is not None or y is not None:
                raise ValueError(
                    "Position is not required. Because it's bot move."
                )
            player.make_move(self._board)  # Bot move
        self._next_turn()

    def _next_turn(self):
        self._turn = Stone.BLACK if self._turn == Stone.WHITE else Stone.WHITE

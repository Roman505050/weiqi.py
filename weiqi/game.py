from typing import Generic

from weiqi.board import BaseBoard
from weiqi.figure import Stone
from weiqi.player import Player, TUser
from weiqi.position import Position


class WeiqiGame(Generic[TUser]):
    def __init__(
        self,
        board: BaseBoard,
        players: list[Player[TUser]],
        turn: Stone | None = None,
    ):
        self._board = board
        self._players = players
        self._turn = turn or Stone.BLACK

        self._validate_players()

    @property
    def board(self) -> BaseBoard:
        return self._board

    @property
    def players(self) -> list[Player[TUser]]:
        return self._players

    @property
    def turn(self) -> Stone:
        return self._turn

    def _validate_players(self):
        if len(self._players) != 2:
            raise ValueError("Game must have exactly 2 players")
        if self._players[0].color == self._players[1].color:
            raise ValueError("Players must have different colors")

    def _validate_current_player(self, player: Player[TUser]):
        if player.color != self.turn:
            raise ValueError("Not your turn")
        if player not in self._players:
            raise ValueError("Player not in game")

    def get_current_player(self) -> Player[TUser]:
        return next(
            player for player in self._players if player.color == self._turn
        )

    def make_move(self, player: Player[TUser], x: int, y: int):
        self._validate_current_player(player)
        position = Position(x, y)
        player.make_move(position, self._board)
        self._next_turn()

    def _next_turn(self):
        self._turn = Stone.BLACK if self._turn == Stone.WHITE else Stone.WHITE

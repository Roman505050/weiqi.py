from typing import Generic
import copy

from weiqi.exceptions import GameOverException
from weiqi.board import Board
from weiqi.figure import Stone
from weiqi.move import MoveHistory, Move
from weiqi.player import Player, TUser
from weiqi.bot import BaseBot


class WeiqiGame(Generic[TUser]):
    def __init__(
        self,
        board: Board,
        player_black: Player[TUser] | BaseBot,
        player_white: Player[TUser] | BaseBot,
        turn: Stone | None = None,
        game_over: bool = False,
        winning_player: Player[TUser] | BaseBot | None = None,
        move_history: MoveHistory | None = None,
    ):
        self._board = board
        self._players = [player_black, player_white]
        self._turn = turn or Stone.BLACK
        self._game_over = game_over
        self._winning_player: Player[TUser] | BaseBot | None = winning_player
        self._move_history = move_history or MoveHistory()

        self._validate_players()
        self._validate_over_game()

    @property
    def board(self) -> Board:
        """Returns a copy of the board."""
        return copy.deepcopy(self._board)

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def players(self) -> list[Player[TUser] | BaseBot]:
        return self._players

    @property
    def winning_player(self) -> Player[TUser] | BaseBot | None:
        return self._winning_player

    @property
    def move_history(self) -> MoveHistory:
        return self._move_history

    @property
    def turn(self) -> Stone:
        return self._turn

    def _validate_over_game(self):
        if self._game_over and not self._winning_player:
            raise ValueError("Winning player is required.")

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

    def resign(self, player: Player[TUser]):
        if self._game_over:
            raise GameOverException("Game is already over.")
        if player not in self._players:
            raise ValueError("Invalid player.")
        self._game_over = True
        self._winning_player = next(pl for pl in self._players if pl != player)

    def make_move(
        self,
        player: Player[TUser] | BaseBot,
        move: Move,
    ):
        if self._game_over:
            raise GameOverException("Game is already over.")

        current_player = self.get_current_player()

        if player != current_player:
            raise ValueError("It's not your turn.")
        if move.figure != player.figure:
            raise ValueError("You can't place a figure of another color.")

        self._board.place_figure(move)
        self._move_history.add_move(move)
        self._next_turn()

    def _next_turn(self):
        self._turn = Stone.BLACK if self._turn == Stone.WHITE else Stone.WHITE

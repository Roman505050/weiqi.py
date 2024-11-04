from typing import Generic
import copy

from weiqi.exceptions import GameOverException
from weiqi.board import Board
from weiqi.enums import Winner
from weiqi.figure import Stone
from weiqi.move import MoveHistory, Move
from weiqi.player import Player, TUser
from weiqi.bot import BaseBot
from weiqi.game_status import GameStatus


class WeiqiGame(Generic[TUser]):
    def __init__(
        self,
        board: Board,
        player_black: Player[TUser] | BaseBot,
        player_white: Player[TUser] | BaseBot,
        turn: Stone | None = None,
        game_status: GameStatus | None = None,
        move_history: MoveHistory | None = None,
        komi: float | int = 6.5,  # 6.5 is the Japanese and Korean rules.
    ):
        self._board = board
        self._players = [player_black, player_white]
        self._turn = turn or Stone.BLACK
        self._game_status = game_status or GameStatus(False, None)
        self._move_history = move_history or MoveHistory()
        self._komi = komi

        self._validate_players()

    @property
    def board(self) -> Board:
        """Returns a copy of the board."""
        return copy.deepcopy(self._board)

    @property
    def game_status(self) -> GameStatus:
        return self._game_status

    @property
    def players(self) -> list[Player[TUser] | BaseBot]:
        return self._players

    @property
    def move_history(self) -> MoveHistory:
        return self._move_history

    @property
    def turn(self) -> Stone:
        return self._turn

    @property
    def komi(self) -> float:
        return self._komi

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
        if self._game_status.is_over:
            raise GameOverException("Game is already over.")
        if player not in self._players:
            raise ValueError("Invalid player.")
        winner = Winner.WHITE if player.figure == Stone.BLACK else Winner.BLACK
        self._game_status.end_game(winner, None, None)

    def make_move(
        self,
        player: Player[TUser] | BaseBot,
        move: Move,
    ):
        if self._game_status.is_over:
            raise GameOverException("Game is already over.")

        current_player = self.get_current_player()

        if player != current_player:
            raise ValueError("It's not your turn.")
        if move.figure != player.figure:
            raise ValueError("You can't place a figure of another color.")

        if move.position is not None:
            self._board.place_figure(move)
        else:
            last_move = self._move_history.last_move
            # If the last move was a pass, the game is over.
            if last_move and last_move.position is None:
                score = self._board.score
                black_score = score[Stone.BLACK]
                white_score = score[Stone.WHITE] + self._komi
                if black_score > white_score:
                    winner = Winner.BLACK
                elif white_score > black_score:
                    winner = Winner.WHITE
                else:
                    winner = Winner.DRAW
                self._game_status.end_game(winner, black_score, white_score)

        self._move_history.add_move(move)
        self._next_turn()

    def _next_turn(self):
        self._turn = Stone.BLACK if self._turn == Stone.WHITE else Stone.WHITE

import unittest

from weiqi.utils.enums import Winner
from weiqi.utils.game_status import GameStatus
from weiqi.core.position import Position
from weiqi.exceptions.game import GameOverException
from weiqi.core.game import WeiqiGame
from weiqi.core.board import Board
from weiqi.players.player import Player
from weiqi.players.bot import RandomBot
from weiqi.core.figure import Stone
from weiqi.core.move import Move


class TestBoard(unittest.TestCase):
    def test_correctly_initializes_game(self):
        board = Board.generate_empty_board(9)
        player: Player = Player(Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)

        game = WeiqiGame(board, player, bot)

        self.assertEqual(game.board.size, 9)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.turn, Stone.BLACK)
        self.assertEqual(game.get_current_player().figure, Stone.BLACK)

        for item in game.players:
            self.assertIsInstance(item, (Player, RandomBot))

    def test_raises_on_not_different_colors(self):
        board = Board.generate_empty_board(9)
        player: Player = Player(Stone.WHITE)
        bot: RandomBot = RandomBot(Stone.WHITE)

        with self.assertRaises(ValueError):
            WeiqiGame(board, player, bot)

    def test_one_player_must_be_human(self):
        board = Board.generate_empty_board(9)
        player: RandomBot = RandomBot(Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)

        with self.assertRaises(ValueError):
            WeiqiGame(board, player, bot)

    def test_raises_on_invalid_player_type(self):
        board = Board.generate_empty_board(9)
        player = "Human"
        bot: RandomBot = RandomBot(Stone.WHITE)

        with self.assertRaises(ValueError):
            WeiqiGame(board, player, bot)  # type: ignore # noqa

    def test_raises_on_not_your_turn(self):
        board = Board.generate_empty_board(9)
        player: Player = Player(Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)

        game = WeiqiGame(board, player, bot)
        with self.assertRaises(ValueError):
            bot.make_move(game)

        player.make_move(game, Position(0, 0))

        with self.assertRaises(ValueError):
            player.make_move(game, Position(0, 1))

    def test_resign(self):
        board = Board.generate_empty_board(9)
        player: Player = Player(Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)

        game = WeiqiGame(board, player, bot)
        self.assertEqual(game.game_status.is_over, False)
        game.resign(player)
        self.assertEqual(game.game_status.is_over, True)
        self.assertEqual(game.game_status.winner, Winner.WHITE)
        self.assertEqual(game.game_status.black_score, None)
        self.assertEqual(game.game_status.white_score, None)
        self.assertEqual(game.get_current_player(), player)

    def test_raises_on_over_game(self):
        board = Board.generate_empty_board(9)
        player: Player = Player(Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)
        game_status = GameStatus(True, Winner.BLACK, 10, 20)
        game = WeiqiGame(board, player, bot, game_status=game_status)

        with self.assertRaises(GameOverException):
            game.resign(player)

        with self.assertRaises(GameOverException):
            player.make_move(game, Position(0, 0))

    def test_raises_on_invalid_use_of_make_move(self):
        board = Board.generate_empty_board(9)
        player_black: Player = Player(Stone.BLACK)
        player_white: Player = Player(Stone.WHITE)
        game = WeiqiGame(board, player_black, player_white)

        with self.assertRaises(ValueError) as context:
            game.make_move(player_white, Move(Position(0, 0), Stone.WHITE))

            self.assertEqual(str(context.exception), "It's not your turn.")

        with self.assertRaises(ValueError) as context:
            game.make_move(player_black, Move(Position(0, 0), Stone.WHITE))

            self.assertEqual(
                str(context.exception),
                "You can't place a figure of another color.",
            )

    def test_history(self):
        board = Board.generate_empty_board(9)
        player_white: Player = Player(Stone.WHITE)
        player_black: Player = Player(Stone.BLACK)
        game = WeiqiGame(
            board, player_black=player_black, player_white=player_white
        )

        player_black.make_move(game, Position(1, 0))
        player_white.make_move(game, Position(0, 1))

        self.assertEqual(len(game.move_history), 2)
        self.assertEqual(game.move_history[0].position, Position(1, 0))
        self.assertEqual(game.move_history[1].position, Position(0, 1))

    def test_two_passes_end_game(self):
        string_state = ".W.../..B../B.W../..BB./.B.B."
        board = Board(string_state)
        player_white: Player = Player(Stone.WHITE)
        player_black: Player = Player(Stone.BLACK)
        game = WeiqiGame(
            board, player_black=player_black, player_white=player_white
        )

        player_black.make_move(game, None)
        player_white.make_move(game, None)

        self.assertEqual(game.game_status.is_over, True)
        self.assertEqual(game.game_status.winner, Winner.WHITE)
        self.assertEqual(game.game_status.black_score, 1)
        self.assertEqual(game.game_status.white_score, 6.5)

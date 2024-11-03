import unittest

from weiqi import Position
from weiqi.exceptions import GameOverException
from weiqi.game import WeiqiGame
from weiqi.board import Board
from weiqi.player import Player
from weiqi.bot import RandomBot
from weiqi.figure import Stone


class TestBoard(unittest.TestCase):
    def test_correctly_initializes_game(self):
        board = Board.generate_empty_board(9)
        player: Player[str] = Player("Human", Stone.BLACK)
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
        player: Player[str] = Player("Human", Stone.WHITE)
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
        player: Player[str] = Player("Human", Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)

        game = WeiqiGame(board, player, bot)
        with self.assertRaises(ValueError):
            game.make_move(bot, 0, 0)

        game.make_move(player, 0, 0)

        with self.assertRaises(ValueError):
            game.make_move(player, 0, 1)

    def test_resign(self):
        board = Board.generate_empty_board(9)
        player: Player[str] = Player("Human", Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)

        game = WeiqiGame(board, player, bot)
        self.assertEqual(game.game_over, False)
        game.resign(player)
        self.assertEqual(game.game_over, True)
        self.assertEqual(game.winning_player, bot)
        self.assertEqual(game.get_current_player(), player)

    def test_raises_on_over_game(self):
        board = Board.generate_empty_board(9)
        player: Player[str] = Player("Human", Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)
        game = WeiqiGame(
            board, player, bot, game_over=True, winning_player=bot
        )

        with self.assertRaises(GameOverException):
            game.resign(player)

        with self.assertRaises(GameOverException):
            game.make_move(player, 0, 0)

    def test_missing_winning_player(self):
        board = Board.generate_empty_board(9)
        player: Player[str] = Player("Human", Stone.BLACK)
        bot: RandomBot = RandomBot(Stone.WHITE)

        with self.assertRaises(ValueError):
            WeiqiGame(board, player, bot, game_over=True)

    def test_history(self):
        board = Board.generate_empty_board(9)
        player_white: Player[str] = Player("White", Stone.WHITE)
        player_black: Player[str] = Player("Black", Stone.BLACK)
        game = WeiqiGame(
            board, player_black=player_black, player_white=player_white
        )

        game.make_move(player_black, 1, 0)
        game.make_move(player_white, 0, 1)

        self.assertEqual(len(game.move_history), 2)
        self.assertEqual(game.move_history[0].position, Position(1, 0))
        self.assertEqual(game.move_history[1].position, Position(0, 1))

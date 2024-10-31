import unittest
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
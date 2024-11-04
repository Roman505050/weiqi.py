# Pygame usage example.
# The old example (Weiqi==0.1.0).
import pygame
import time
import sys

from weiqi import WeiqiGame, Board, Player, Stone, Position, BaseBot, RandomBot


class WeiqiGUI:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BOARD_COLOR = (222, 184, 135)
    LINE_COLOR = BLACK

    def __init__(self, game: WeiqiGame, player: Player, bot: BaseBot):
        pygame.font.init()
        self.game = game
        self.player = player
        self.bot = bot
        self.board_size = game.board.size
        self.cell_size = 40
        self.window_size = self.cell_size * (self.board_size + 1)
        self.screen = pygame.display.set_mode(
            (self.window_size, self.window_size + 60)
        )
        pygame.display.set_caption("Weiqi")

    def draw(self):
        self._draw_background()
        self._draw_board(self.game.board.state_as_matrix)
        self._draw_score(self.game.board.score)
        self._draw_turn(self.game.turn)
        pygame.display.flip()

    @property
    def _front_size(self) -> int:
        mapping = {
            5: 25,
            6: 25,
            7: 25,
        }
        return mapping.get(self.board_size, 30)

    def _draw_board(self, board: list[list[int]]):
        """Initialize the board by state in the game"""

        for x in range(self.board_size):
            for y in range(self.board_size):
                center_x = x * self.cell_size + self.cell_size
                center_y = y * self.cell_size + self.cell_size
                if board[y][x] == -1:
                    pygame.draw.circle(
                        self.screen,
                        self.WHITE,
                        (center_x, center_y),
                        15,
                    )
                elif board[y][x] == 1:
                    pygame.draw.circle(
                        self.screen,
                        self.BLACK,
                        (center_x, center_y),
                        15,
                    )

    def _draw_score(self, score: dict[Stone, int]):
        """Draw the score"""
        font = pygame.font.Font(None, self._front_size)
        text = font.render(
            f"Black: {score[Stone.BLACK]} White: {score[Stone.WHITE]}",
            True,
            self.BLACK,
        )
        self.screen.blit(text, (10, self.window_size))

    def _draw_turn(self, turn: Stone):
        """Draw the current turn"""
        font = pygame.font.Font(None, self._front_size)
        text = font.render(
            f"{'Black' if turn == Stone.BLACK else 'White'}'s turn",
            True,
            self.BLACK,
        )
        self.screen.blit(text, (10, self.window_size + 30))

    def _draw_background(self):
        """Draw the board grid"""
        STAR_POINTS_MAP = {
            5: [],
            6: [],
            7: [],
            8: [],
            9: [(3, 3), (3, 7), (7, 3), (7, 7)],
            11: [(3, 3), (3, 9), (9, 3), (9, 9), (6, 6)],
            13: [(4, 4), (4, 10), (10, 4), (10, 10), (7, 7)],
            15: [(4, 4), (4, 12), (12, 4), (12, 12), (8, 8)],
            17: [(4, 4), (4, 14), (14, 4), (14, 14), (10, 10)],
            19: [
                (4, 4),
                (4, 16),
                (16, 4),
                (16, 16),
                (10, 10),
                (4, 10),
                (10, 4),
                (10, 16),
                (16, 10),
            ],
        }
        self.screen.fill(self.BOARD_COLOR)

        for i in range(self.board_size):
            pygame.draw.line(
                self.screen,
                self.LINE_COLOR,
                (self.cell_size, self.cell_size * (i + 1)),
                (self.window_size - self.cell_size, self.cell_size * (i + 1)),
                2,
            )
            pygame.draw.line(
                self.screen,
                self.LINE_COLOR,
                (self.cell_size * (i + 1), self.cell_size),
                (self.cell_size * (i + 1), self.window_size - self.cell_size),
                2,
            )

        star_points = STAR_POINTS_MAP.get(self.board_size, [])
        for x, y in star_points:
            pygame.draw.circle(
                self.screen,
                self.LINE_COLOR,
                (x * self.cell_size, y * self.cell_size),
                5,
            )

    def place_stone(self, x: int, y: int) -> None:
        """Place a stone on the board"""
        try:
            self.player.make_move(self.game, Position(x, y))
            self.draw()

            self.bot_move()
        except ValueError as e:
            print(f"Invalid move: {e}")

    def bot_move(self) -> None:
        try:
            player = self.game.get_current_player()
            if isinstance(player, BaseBot):
                time.sleep(1)
                player.make_move(self.game)
                self.draw()
        except ValueError as e:
            if "can't find a valid move" in str(e):
                print("Bot can't find a valid move. Game over.")
                sys.exit()
            print(f"Invalid move: {e}")

    def main_loop(self):
        self.draw()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x = (x - self.cell_size // 2) // self.cell_size
                    y = (y - self.cell_size // 2) // self.cell_size

                    self.place_stone(x, y)


def main():
    available_sizes = [5, 6, 7, 8, 9, 11, 13, 15, 17, 19]
    while True:
        try:
            board_size = int(
                input(
                    "Enter the board size "
                    f"({', '.join(map(str, available_sizes))}): "
                )
            )
            if board_size not in available_sizes:
                raise ValueError
            break
        except ValueError:
            print("Invalid size")
    board_init = Board.generate_empty_board(board_size)
    player = Player("Human", Stone.BLACK)
    bot = RandomBot(Stone.WHITE)
    game_ist = WeiqiGame(board_init, player, bot, turn=Stone.BLACK)
    gui = WeiqiGUI(game=game_ist, player=player, bot=bot)
    gui.main_loop()


if __name__ == "__main__":
    main()

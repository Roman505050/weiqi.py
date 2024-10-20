# Pygame usage example
from dataclasses import dataclass

from weiqi import WeiqiGame, Board, Player, Stone

import pygame
import sys


class WeiqiGUI:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BOARD_COLOR = (222, 184, 135)
    LINE_COLOR = BLACK

    def __init__(self, game: WeiqiGame):
        self.game = game
        self.board_size = game.board.size
        self.cell_size = 40
        self.window_size = self.cell_size * (self.board_size + 1)
        self.screen = pygame.display.set_mode(
            (self.window_size, self.window_size)
        )
        pygame.display.set_caption("Weiqi")

    def _draw_board(self, board: list[list[int]]):
        """Initialize the board by state in the game"""
        self._draw_background()

        for x in range(self.board_size):
            for y in range(self.board_size):
                center_x = x * self.cell_size + self.cell_size
                center_y = y * self.cell_size + self.cell_size
                if board[x][y] == 0:
                    pygame.draw.circle(
                        self.screen,
                        self.WHITE,
                        (center_x, center_y),
                        15,
                    )
                elif board[x][y] == 1:
                    pygame.draw.circle(
                        self.screen,
                        self.BLACK,
                        (center_x, center_y),
                        15,
                    )

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

    def place_stone(self, x: int, y: int):
        """Place a stone on the board"""
        try:
            player = self.game.get_current_player()
            self.game.make_move(player, x, y)
            self._draw_board(self.game.board.state)
        except ValueError as e:
            print(f"Invalid move: {e}")

    def main_loop(self):
        self._draw_board(self.game.board.state)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x = (x - self.cell_size // 2) // self.cell_size
                    y = (y - self.cell_size // 2) // self.cell_size

                    self.place_stone(x, y)
            pygame.display.flip()


@dataclass
class User:
    id: int
    name: str


def main():
    available_sizes = [5, 6, 7, 8, 9, 11, 13, 15, 17, 19]
    while True:
        try:
            board_size = int(
                input(
                    "Enter the board size "
                    f"({", ".join(map(str, available_sizes))}): "
                )
            )
            if board_size not in available_sizes:
                raise ValueError
            break
        except ValueError:
            print("Invalid size")
    board_init = Board.generate_empty_board(board_size)
    players: list[Player[User]] = [
        Player(User(1, "Alice"), Stone.BLACK),
        Player(User(2, "Bob"), Stone.WHITE),
    ]
    game_ist = WeiqiGame(board_init, players, Stone.BLACK)
    gui = WeiqiGUI(game_ist)
    gui.main_loop()


if __name__ == "__main__":
    main()

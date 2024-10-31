from itertools import product

from weiqi.group import Group
from weiqi.position import Position
from weiqi.figure import Stone
from weiqi.move import Move


class Board:
    """Class for the board of the Weiqi game."""

    def __init__(
        self,
        figures: dict[Position, Stone | None] | str | list[list[int]],
    ):
        if isinstance(figures, str):
            self._figures = self._from_string(figures)
        elif isinstance(figures, list):
            self._figures = self._from_matrix(figures)
        else:
            self._figures = figures

        self._size = int(len(self._figures) ** 0.5)

        if not self._validate_available_size():
            raise ValueError("Not available size.")
        if not self._validate_positions():
            raise ValueError("Invalid positions.")
        if not self._is_square_board():
            raise ValueError("Board must be square.")
        if not self._validate_figures():
            raise ValueError("Invalid figures.")

        for group in self._find_groups_without_liberties():
            self.__remove_group(group)

    @property
    def figures(self) -> dict[Position, Stone | None]:
        return self._figures

    @property
    def size(self) -> int:
        return self._size

    def _is_square_board(self) -> bool:
        unique_x = len(set(position.x for position in self._figures.keys()))
        unique_y = len(set(position.y for position in self._figures.keys()))
        return unique_x == unique_y and unique_x == self._size

    def _validate_positions(self) -> bool:
        return all(
            position.x < self._size and position.y < self._size
            for position in self._figures.keys()
        )

    def _validate_figures(self) -> bool:
        return all(
            isinstance(stone, (Stone, type(None)))
            for stone in self._figures.values()
        )

    def _validate_available_size(self) -> bool:
        valid_sizes = {5, 6, 7, 8, 9, 11, 13, 15, 17, 19}
        return self.size in valid_sizes

    def position_in_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self._size and 0 <= position.y < self._size

    def _find_groups_without_liberties(self) -> list[Group]:
        return [
            self._group_at_position(position)
            for position in self._get_not_empty_positions()
            if not self._group_at_position(position).liberties
        ]

    def _get_not_empty_positions(self) -> list[Position]:
        return [
            position
            for position, stone in self._figures.items()
            if stone is not None
        ]

    def _get_neighbors(self, position: Position) -> list[Position]:
        return [
            position + delta
            for delta in [
                Position(0, 1),
                Position(0, -1),
                Position(1, 0),
                Position(-1, 0),
            ]
            if self.position_in_bounds(position + delta)
        ]

    def __remove_group(self, group: Group):
        for position in group.positions:
            self._figures[position] = None

    def _group_at_position(self, position: Position) -> Group:
        figure = self._figures.get(position, None)
        if figure is None:
            raise ValueError("Position is empty.")

        def bfs(queue: list[Position], visited: set[Position], group: Group):
            while queue:
                pos = queue.pop(0)
                if pos in visited:
                    continue
                visited.add(pos)

                if self._figures.get(pos) == figure:
                    group.positions.add(pos)
                    queue.extend(
                        neighbor
                        for neighbor in self._get_neighbors(pos)
                        if neighbor not in visited
                    )
                elif self._figures.get(pos) is None:
                    group.liberties.add(pos)
            return group

        group = Group(positions=set(), liberties=set(), figure=figure)
        return bfs([position], set(), group)

    @staticmethod
    def generate_empty_board(size: int) -> "Board":
        figures: dict[Position, Stone | None] = {
            Position(x, y): None for x, y in product(range(size), range(size))
        }
        return Board(figures)

    @property
    def state_as_matrix(self) -> list[list[int]]:
        """
        Converts the board state to a matrix representation.

        -1 - white stone
        0 - empty intersection
        1 - black stone

        Returns:
            list[list[int]]: The board state as a matrix.
        """
        state = [[0] * self.size for _ in range(self.size)]
        for position, stone in self._figures.items():
            state[position.y][position.x] = (
                1
                if stone == Stone.BLACK
                else -1 if stone == Stone.WHITE else 0
            )
        return state

    @property
    def state_as_string(self) -> str:
        """
        Converts the board state to a string representation.

        W - white stone
        B - black stone
        . - empty intersection

        Returns:
            str: The board state as a string.
        """
        symbols = {Stone.BLACK: "B", Stone.WHITE: "W", None: "."}
        return "/".join(
            "".join(
                symbols.get(self._figures.get(Position(x, y)), ".")
                for y in range(self.size)
            )
            for x in range(self.size)
        )

    @staticmethod
    def _from_matrix(matrix: list[list[int]]) -> dict[Position, Stone | None]:
        return {
            Position(x, y): (
                Stone.BLACK
                if cell == 1
                else Stone.WHITE if cell == -1 else None
            )
            for y, row in enumerate(matrix)
            for x, cell in enumerate(row)
        }

    @staticmethod
    def _from_string(string: str) -> dict[Position, Stone | None]:
        return Board._from_matrix(
            [
                [
                    1 if cell == "B" else -1 if cell == "W" else 0
                    for cell in row
                ]
                for row in string.split("/")
            ]
        )

    def place_figure(self, move: Move) -> None:
        if not self.position_in_bounds(move.position):
            raise ValueError("Position out of bounds.")
        if self._figures.get(move.position) is not None:
            raise ValueError("Intersection occupied by existing stone.")

        self._figures[move.position] = move.figure

        try:
            neighboring_enemy_groups = [
                self._group_at_position(neighbor)
                for neighbor in self._get_neighbors(move.position)
                if self._figures.get(neighbor) not in {None, move.figure}
            ]

            for group in neighboring_enemy_groups:
                if not group.liberties:
                    self.__remove_group(group)

            new_group = self._group_at_position(move.position)
        except ValueError as e:
            self._figures[move.position] = None
            raise e

        if not new_group.liberties:
            self._figures[move.position] = None
            raise ValueError("New group has zero liberties (suicide)")

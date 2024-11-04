from weiqi.enums import Winner


class GameStatus:
    def __init__(
        self,
        is_over: bool,
        winner: Winner | None,
        black_score: int | None = None,
        white_score: float | int | None = None,
    ):
        self._is_over = is_over
        self._winner = winner

        self._validate_over_game()
        self._validate_scores(black_score, white_score)

        self._black_score = black_score
        self._white_score = white_score

    @property
    def is_over(self) -> bool:
        return self._is_over

    @property
    def winner(self) -> Winner | None:
        return self._winner

    @property
    def black_score(self) -> int | None:
        return self._black_score

    @property
    def white_score(self) -> float | int | None:
        return self._white_score

    def _validate_over_game(self):
        if self._is_over and self._winner is None:
            raise ValueError("Game is over but no winner is set.")

    @staticmethod
    def _validate_scores(
        black_score: int | None, white_score: float | int | None
    ):
        if (black_score is not None) != (white_score is not None):
            raise ValueError("Both scores cannot be set at the same time.")

    def end_game(
        self,
        winner: Winner,
        black_score: int | None,
        white_score: float | int | None,
    ):
        self._is_over = True
        self._winner = winner

        self._validate_scores(black_score, white_score)
        self._black_score = black_score
        self._white_score = white_score

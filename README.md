# weiqi.py - Library for the game of Go

This is a library for the game of Go. It is written in Python and is designed to be easy to understand and use. It is also designed to be easy to extend and modify.

### Usage

To use this library, you need to have Python installed on your computer.

To install the library, you can use the following command:

```
pip install weiqi
```

To use the library, you can import it in your Python code like this:

```python
from weiqi import Board, WeiqiGame, Player, Stone

# Example user implementation
class User:
    def __init__(self, name: str):
        self.name = name

player_black = Player(User("Black"), Stone.BLACK)
player_white = Player(User("White"), Stone.WHITE)

# 19x19 board
board = Board.generate_empty_board(19)

game: WeiqiGame[User] = WeiqiGame(
    player_black=player_black,
    player_white=player_white,
    board=board
)

# Then you can implement user interaction with the game 
# through various interfaced (Example: CLI, GUI, etc.)
# You can also implement AI players
```

### Testing

To run the tests, you can use the following command:

```
python -m unittest discover -s tests
```

### Example

<img src="example/example.png" alt="Example of the library in use" width="400"/>

You can see an example with a simple Pygame GUI in the `example/pygame_example.py` file.

For starting the example, you can run the following command:
```
poetry install --only example
python example/pygame_example.py
```

After running the command, you should see a window pop up with a Go board. You can click on the board to place stones.

### TODO

- [ ] Implement the pass move system
- [ ] Implement the surrender system
- [ ] Implement the time control system
- [x] Implement the count of captured stones
- [ ] Implement the end-game detection
- [x] Implement the simple scoring system
- [ ] Implement the complex scoring system
- [ ] Implement the game history
- [ ] Implement the AI players
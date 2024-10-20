from weiqi.position import Position


class Group:
    def __init__(self, stones: set[Position], liberties: set[Position]):
        self.stones = stones
        self.liberties = liberties

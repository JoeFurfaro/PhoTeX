class Vector2:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: object) -> object:
        if isinstance(other, self.__class__):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError
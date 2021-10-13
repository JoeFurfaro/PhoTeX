class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return abs(self.x - other.x) < 1e-6 and abs(self.y - other.y) < 1e-6
        else:
            return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: object) -> object:
        if isinstance(other, self.__class__):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError
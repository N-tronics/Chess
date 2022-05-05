# Vector Classes
# Nischay Bharadwaj (N-tronics)

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self) -> tuple:
        return self.x, self.y

    def __sub__(self, sub):
        return Vec2(self.x - sub.x, self.y - sub.y) if isinstance(sub, Vec2) else Vec2(self.x - sub, self.y - sub)

    def __add__(self, add):
        return Vec2(self.x + add.x, self.y + add.y) if isinstance(add, Vec2) else Vec2(self.x + add, self.y + add)

    def __mul__(self, mul):
        return Vec2(self.x * mul.x, self.y * mul.y) if isinstance(mul, Vec2) else Vec2(self.x * mul, self.y * mul)

    def __eq__(self, vec):
        if not isinstance(vec, Vec2):
            raise ValueError(f"{vec} not a Vec2")
        return self.x == vec.x and self.y == vec.y

    def __repr__(self):
        return f'[{self.x} {self.y}]'

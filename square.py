# Square Class
# Nischay Bharadwaj (N-tronics)

from typing import *
from vector import *
from pieces import BasePiece
from game_constants import Piece


class Square:
    def __init__(self, pos: Vec2, color: Piece.Color):
        self.pos = pos
        self.color = color
        self.piece: BasePiece | None = None
        self.attacks: Dict[Piece.Color, int] = {
            Piece.WHITE: 0,
            Piece.BLACK: 0
        }

    def has_piece(self) -> bool:
        """
        Checks whether the square has a piece
        :return:
        """
        return self.piece is not None

    def square_color(self) -> Piece.Color:
        """
        Returns the color of the square
        :return: Color
        """
        return Piece.WHITE if (self.pos.x + self.pos.y) % 2 == 0 else Piece.BLACK

    def __repr__(self):
        return f"<S {self.color} at {self.pos}>"

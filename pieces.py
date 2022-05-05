# Piece Classes
# Nischay Bharadwaj (N-tronics)

import numpy as np
from game_constants import Piece, dir_offsets
from square import Square
from typing import *
from vector import *


class BasePiece:
    @staticmethod
    def compute_raw_moves(pos: Vec2, offsets: List[Vec2], depth: int) -> Iterator[Vec2]:
        """
        Generates a list of valid squares that a piece can move to
        :param pos: Current position of piece
        :param offsets: List of offsets
        :param depth: Number of times to check in each offset
        :return: Generator of a move
        """
        for ofst in offsets:
            for i in range(depth):
                sqr = pos + ofst * i
                if 0 <= sqr.x <= 7 and 0 <= sqr.y <= 7:
                    yield sqr

    @staticmethod
    def get_name(type_: Piece.Type) -> str:
        if type_ == Piece.KING:
            return "king"
        elif type_ == Piece.QUEEN:
            return "queen"
        elif type_ == Piece.ROOK:
            return "rook"
        elif type_ == Piece.BISHOP:
            return "bishop"
        elif type_ == Piece.KNIGHT:
            return "knight"
        elif type_ == Piece.PAWN:
            return "pawn"

    def __init__(self, pos: Vec2, color: Piece.Color, type_: Piece.Type):
        self.pos = pos
        self.color = color
        self.type = type_

        self.selected = False
        self.valid_moves: List[Vec2] = []

    def is_white(self):
        return self.color == Piece.WHITE

    def __repr__(self):
        return f"<P {'White' if self.is_white() else 'Black'} {BasePiece.get_name(self.type)} at {self.pos}>"


class King(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.KING)

    def compute_valid_moves(self, board: np.ndarray) -> None:
        """
        Computes valid moves for a King
        :param board: Current board array
        :return: None
        """
        for sqr_coords in BasePiece.compute_raw_moves(self.pos, dir_offsets["cross"], 1):
            sqr: Square = board[sqr_coords.x, sqr_coords.y]
            if sqr.has_piece():
                pass


class Queen(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.QUEEN)


class Rook(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.ROOK)


class Bishop(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.BISHOP)


class Knight(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.KNIGHT)


class Pawn(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.PAWN)


def create_piece(type_: Piece.Type) -> Type:
    """
    Returns a piece class according to the type
    :param type_: Type of the piece
    :return: Type[Piece]
    """
    if type_ == Piece.KING:
        return King
    elif type_ == Piece.QUEEN:
        return Queen
    elif type_ == Piece.ROOK:
        return Rook
    elif type_ == Piece.BISHOP:
        return Bishop
    elif type_ == Piece.KNIGHT:
        return Knight
    elif type_ == Piece.PAWN:
        return Pawn

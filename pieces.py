# Piece Classes
# Nischay Bharadwaj (N-tronics)

import numpy as np
from typing import *
from vector import *

PieceColor = str
PieceType = str

offsets: Dict[str, List[Vec2]] = {
    "cross": [
        Vec2(0, -1),  # Up
        Vec2(0, 1),  # Down
        Vec2(1, 0),  # Right
        Vec2(-1, 0)  # Left
    ],
    "diagonal": [
        Vec2(-1, -1),  # Up left
        Vec2(1, -1),  # Up right
        Vec2(1, 1),  # Down right
        Vec2(-1, 1)  # Down left
    ],
    "knight": [
        Vec2(-2, -1), Vec2(-1, -2),
        Vec2(1, -2), Vec2(2, -1),
        Vec2(2, 1), Vec2(1, 2),
        Vec2(-1, 2), Vec2(-2, 1)
    ]
}


class Piece:
    WHITE = "w"
    BLACK = "b"
    KING = "k"
    QUEEN = "q"
    ROOK = "r"
    BISHOP = "b"
    KNIGHT = "n"
    PAWN = "p"

    @staticmethod
    def compute_raw_moves(piece, board: np.ndarray, offset: List[Vec2], depth: int) -> List[Vec2]:
        moves: List[Vec2] = []
        for ofst in offset:
            for i in range(depth):
                sqr = piece.pos + ofst * i
                if sqr.x < 0 or sqr.x > 7 or sqr.y < 0 or sqr.y > 7:
                    break
                p = board[sqr.x, sqr.y]
                if p == 0:
                    moves.append(sqr)
                elif p.color != piece.color:
                    moves.append(sqr)
                    break
                else:
                    break
        return moves

    @staticmethod
    def get_name(type_: PieceType) -> str:
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

    def __init__(self, pos: Vec2, color: PieceColor, type_: PieceType):
        self.pos = pos
        self.color = color
        self.type = type_

        self.selected = False
        self.valid_moves: List[Vec2] = []

    def is_white(self):
        return self.color == Piece.WHITE

    def __repr__(self):
        return f"<P {'White' if self.is_white() else 'Black'} {Piece.get_name(self.type)} at {self.pos}>"


class King(Piece):
    def __init__(self, pos: Vec2, color: PieceColor):
        super().__init__(pos, color, Piece.KING)


class Queen(Piece):
    def __init__(self, pos: Vec2, color: PieceColor):
        super().__init__(pos, color, Piece.QUEEN)


class Rook(Piece):
    def __init__(self, pos: Vec2, color: PieceColor):
        super().__init__(pos, color, Piece.ROOK)


class Bishop(Piece):
    def __init__(self, pos: Vec2, color: PieceColor):
        super().__init__(pos, color, Piece.BISHOP)


class Knight(Piece):
    def __init__(self, pos: Vec2, color: PieceColor):
        super().__init__(pos, color, Piece.KNIGHT)


class Pawn(Piece):
    def __init__(self, pos: Vec2, color: PieceColor):
        super().__init__(pos, color, Piece.PAWN)


def create_piece(type_: PieceType) -> Type:
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

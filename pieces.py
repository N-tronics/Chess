# Piece Classes
# Nischay Bharadwaj (N-tronics)

import numpy as np
from typing import *
from vector import *

PieceColor = str
PieceType = str

offsets: Dict[str, List[Vec2]] = {
    "cross": [
        Vec2(0, -1),    # Up
        Vec2(0, 1),     # Down
        Vec2(1, 0),     # Right
        Vec2(-1, 0)     # Left
    ],
    "diagonal": [
        Vec2(-1, -1),    # Up left
        Vec2(1, -1),     # Up right
        Vec2(1, 1),     # Down right
        Vec2(-1, 1)      # Down left
    ],
    "knight": [
        Vec2(-2, -1), Vec2(-1, -2),
        Vec2(1, -2), Vec2(2, -1),
        Vec2(2, 1), Vec2(1, 2),
        Vec2(-1, 2), Vec2(-2, 1)
    ]
}


class Piece:
    WTE = "w"
    BLK = "b"
    KNG = "k"
    QEN = "q"
    ROK = "r"
    BSP = "b"
    KNT = "n"
    PWN = "p"

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
        if type_ == Piece.KNG:
            return "king"
        elif type_ == Piece.QEN:
            return "queen"
        elif type_ == Piece.ROK:
            return "rook"
        elif type_ == Piece.BSP:
            return "bishop"
        elif type_ == Piece.KNT:
            return "knight"
        elif type_ == Piece.PWN:
            return "pawn"

    def __init__(self, pos: Vec2, color: PieceColor, type_: PieceType):
        self.pos = pos
        self.color = color
        self.type = type_

        self.selected = False
        self.valid_moves: List[Vec2] = []

    def is_white(self):
        return self.color == Piece.WTE

    def __repr__(self):
        return f"<P {'White' if self.is_white() else 'Black'} {Piece.get_name(self.type)} at {self.pos}>"


class King(Piece):
    def __init__(self, pos: Vec2, color: PieceColor):
        super().__init__(pos, color, Piece.KNG)

    def compute_valid_moves(self, board: np.ndarray):
        self.valid_moves = Piece.compute_raw_moves(self, board, offsets["cross"], 1)
        self.valid_moves.extend(Piece.compute_raw_moves(self, board, offsets["diagonal"], 1))

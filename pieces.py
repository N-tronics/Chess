# Piece Classes
# Nischay Bharadwaj (N-tronics)

import numpy as np
from game_constants import Piece, dir_offsets
from square import Square
from typing import *
from vector import *


class BasePiece:
    @staticmethod
    def generate_raw_moves(pos: Vec2, offsets: List[Vec2], depth: int = 8) -> Generator[Vec2, bool, None]:
        """
        Generates a list of valid squares that a piece can move to
        :param pos: Current position of piece
        :param offsets: List of offsets
        :param depth: Number of times to check in each offset
        :return: Generator of a move
        """
        for ofst in offsets:
            for i in range(1, depth + 1):
                sqr_coords = pos + ofst * i
                if 0 <= sqr_coords.x <= 7 and 0 <= sqr_coords.y <= 7:
                    if (yield sqr_coords):
                        return

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

        self.selected: bool = False
        self.stop_iteration: bool = False
        self.valid_moves: List[Vec2] = []

    def compute_raw_moves(self, offsets: List[Vec2], depth: int) -> Generator[Vec2, None, None]:
        """
        Wrapper around BasePiece.generate_raw_moves
        :param offsets: List of offsets
        :param depth: Number of times to check in each offset
        :return:
        """
        raw_moves_gen = BasePiece.generate_raw_moves(self.pos, offsets, depth)
        try:
            next_sqr_coords = next(raw_moves_gen)
            while next_sqr_coords:
                yield next_sqr_coords
                next_sqr_coords = raw_moves_gen.send(self.stop_iteration)
        except StopIteration:
            pass

        self.stop_iteration = False

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
        self.valid_moves.clear()
        for sqr_coords in self.compute_raw_moves(dir_offsets["cross"], 1):
            sqr: Square = board[sqr_coords.x, sqr_coords.y]
            if sqr.has_piece():
                if sqr.piece.color != self.color:
                    self.valid_moves.append(sqr_coords)
            else:
                self.valid_moves.append(sqr_coords)


class Queen(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.QUEEN)

    def compute_valid_moves(self, board: np.ndarray) -> None:
        """
        Computes valid moves for a Queen
        :param board: Current board array
        :return: None
        """


class Rook(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.ROOK)

    def compute_valid_moves(self, board: np.ndarray) -> None:
        """
        Computes valid moves for a Rook
        :param board: Current board array
        :return: None
        """


class Bishop(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.BISHOP)

    def compute_valid_moves(self, board: np.ndarray) -> None:
        """
        Computes valid moves for a Bishop
        :param board: Current board array
        :return: None
        """


class Knight(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.KNIGHT)

    def compute_valid_moves(self, board: np.ndarray) -> None:
        """
        Computes valid moves for a Knight
        :param board: Current board array
        :return: None
        """


class Pawn(BasePiece):
    def __init__(self, pos: Vec2, color: Piece.Color):
        super().__init__(pos, color, Piece.PAWN)

    def compute_valid_moves(self, board: np.ndarray) -> None:
        """
        Computes valid moves for a Pawn
        :param board: Current board array
        :return: None
        """


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

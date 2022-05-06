# Game Constants
# Nischay Bharadwaj (N-tronics)

from dataclasses import dataclass
from vector import Vec2
from typing import *


@dataclass
class Piece:
    Color = str
    Type = str

    WHITE = "w"
    BLACK = "b"
    KING = "k"
    QUEEN = "q"
    ROOK = "r"
    BISHOP = "b"
    KNIGHT = "n"
    PAWN = "p"


@dataclass
class PColors:
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    ORANGE_HL = (246, 156, 110)
    RED_HL = (248, 109, 92)


dir_offsets: Dict[str, List[Vec2]] = {
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

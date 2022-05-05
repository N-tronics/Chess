# Chess board maintenance class
# Nischay Bharadwaj (N-tronics)

from pieces import *

power_pieces: List[PieceType] = [Piece.ROK, Piece.KNT, Piece.BSP, Piece.QEN, Piece.KNG, Piece.BSP, Piece.KNT, Piece.ROK]
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Square:
    def __init__(self, pos: Vec2, color: PieceColor):
        self.pos = pos
        self.color = color
        self.piece: Piece | None = None
        self.attacks: Dict[PieceColor, int] = {
            Piece.WTE: 0,
            Piece.BLK: 0
        }

    def has_piece(self) -> bool:
        """
        Checks whether the square has a piece
        :return:
        """
        return self.piece is not None

    def __repr__(self):
        return f"<S {self.color} at {self.pos}>"


class ChessBoard:
    def __init__(self):
        self.board: np.ndarry = np.empty((8, 8), dtype=Square)
        print(self.board)
        for i in range(8):
            for j in range(8):
                self.board[i, j] = Square(Vec2(i, j), Piece.WTE if (i + j) % 2 == 0 else Piece.BLK)
        print(self.board)

        self.piece_positions: Dict[str, List[Vec2]] = {
            Piece.WTE: [],
            Piece.BLK: []
        }
        self.turn: PieceColor = Piece.WTE
        self.selected_square: Square | None = None

        self.load_fen(start_fen)

    def load_fen(self, fen: str) -> None:
        """
        Loads a FEN string
        :param fen: str
        :return: None
        """
        fields = fen.split()

        # Piece Position
        for i, row in enumerate(fields[0].split("/")):
            j = 0
            while j < len(row):
                if row[j].isnumeric():
                    for j in range(j, j + int(row[j])):
                        self.board[j, i].piece = None
                else:
                    color = Piece.WTE if row[j].isupper() else Piece.BLK
                    self.piece_positions[color].append(Vec2(j, i))
                    self.board[j, i].piece = Piece(Vec2(j, i), color, row[j].lower())
                    j += 1

    @staticmethod
    def valid_coords(coords: Vec2) -> bool:
        """
        Checks whether the given coordinates are within bounds
        :param coords: Vec2(grid X coordinate, grid Y coordinate)
        :return: bool
        """
        return 0 <= coords.x <= 7 and 0 <= coords.y <= 7

    def select(self, coords: Vec2 | None) -> None:
        """
        Selects a square
        :param coords: Vec2(grid X coordinate, grid Y coordinate) | None for deselecting
        :return: None
        """
        if self.selected_square is not None:
            self.selected_square.piece.selected = False

        if coords is None:
            self.selected_square = None
        else:
            self.selected_square = self.board[coords.x, coords.y]
            self.selected_square.piece.selected = True

    def handle_click(self, pos: Vec2) -> None:
        """
        Handles a click event on a square
        :param pos: Vec2(grid X coordinate, grid Y coordinate)
        :return: None
        """
        sqr_clicked: Square = self.board[pos.x, pos.y]
        # TODO: Valid moves takes precedence over reselection
        if not sqr_clicked.has_piece():
            self.select(None)
        else:
            self.select(pos)

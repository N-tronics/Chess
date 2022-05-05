# Chess board maintenance class
# Nischay Bharadwaj (N-tronics)

from pieces import *

power_pieces: List[PieceType] = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Square:
    def __init__(self, pos: Vec2, color: PieceColor):
        self.pos = pos
        self.color = color
        self.piece: Piece | None = None
        self.attacks: Dict[PieceColor, int] = {
            Piece.WHITE: 0,
            Piece.BLACK: 0
        }

    def has_piece(self) -> bool:
        """
        Checks whether the square has a piece
        :return:
        """
        return self.piece is not None

    def __repr__(self):
        return f"<S {self.color} at {self.pos}>"


class ChessEngine:
    def __init__(self):
        # This array is the internal representation of a chess board
        self.board: np.ndarry = np.empty((8, 8), dtype=Square)
        for i in range(8):
            for j in range(8):
                self.board[i, j] = Square(Vec2(i, j), Piece.WHITE if (i + j) % 2 == 0 else Piece.BLACK)

        # Keeps track of piece position according to color to avoid a board search
        self.piece_positions: Dict[str, List[Vec2]] = {
            Piece.WHITE: [],
            Piece.BLACK: []
        }
        self.turn: PieceColor = Piece.WHITE
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
                # Remove pieces at empty squares
                if row[j].isnumeric():
                    for j in range(j, j + int(row[j])):
                        self.board[j, i].piece = None
                # Place a pieces
                else:
                    color = Piece.WHITE if row[j].isupper() else Piece.BLACK
                    self.piece_positions[color].append(Vec2(j, i))
                    self.board[j, i].piece = create_piece(row[j].lower())(Vec2(j, i), color)
                    j += 1

        # Turn
        self.turn = Piece.WHITE if fields[1] == "w" else Piece.BLACK

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
        :param coords: Vec2(grid X coordinate, grid Y coordinate) | None to deselect
        :return: None
        """
        # If a square was previously selected, deselect it
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
        if sqr_clicked.has_piece():
            self.select(pos)
        else:
            self.select(None)

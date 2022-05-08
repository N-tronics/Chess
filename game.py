# Chess board maintenance class
# Nischay Bharadwaj (N-tronics)

from pieces import *
from square import Square

power_pieces: List[Piece.Type] = [
    Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK
]
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
empty_fen = "8/8/8/8/8/8/8/8 w KQkq - 0 1"


class ChessEngine:
    def __init__(self, load_start_fen: bool = True):
        # This array is the internal representation of a chess board
        self.board: np.ndarry = np.empty((8, 8), dtype=Square)
        for i in range(8):
            for j in range(8):
                self.board[i, j] = Square(Vec2(i, j), Piece.WHITE if (i + j) % 2 == 0 else Piece.BLACK)

        # Keeps track of piece position according to color to avoid a board search
        self.piece_positions: Dict[str, Set[Vec2]] = {
            Piece.WHITE: set([]),
            Piece.BLACK: set([])
        }
        self.turn: Piece.Color = Piece.WHITE
        self.selected_square: Square | None = None

        if load_start_fen:
            self.load_fen(start_fen)
        self.load_fen("8/2npp3/1Qb5/5B2/8/4q3/2PP1N2/8 w KQkq - 0 1")

    def clear_board(self):
        self.load_fen(empty_fen)

    def load_fen(self, fen: str) -> None:
        """
        Loads a FEN string
        :param fen: str
        :return: None
        """
        fields = fen.split()
        self.piece_positions[Piece.WHITE].clear()
        self.piece_positions[Piece.BLACK].clear()

        # Piece Position
        for i, row in enumerate(fields[0].split("/")):
            j = 0
            for k in row:
                if k.isnumeric():
                    for _ in range(j, j + int(k)):
                        self.board[_, i].piece = None
                    j += int(k)
                else:
                    color = Piece.WHITE if k.isupper() else Piece.BLACK
                    self.piece_positions[color].add(Vec2(j, i))
                    self.place_piece(Vec2(j, i), k.lower(), color)
                    j += 1

        # Turn
        self.turn = Piece.WHITE if fields[1] == "w" else Piece.BLACK

    def generate_fen(self):
        fen = ""
        # Pieces
        for i in range(8):
            empty = 0
            for j in range(8):
                sqr = self.board[j, i]
                if sqr.has_piece():
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += sqr.piece.type.upper() if sqr.piece.color == Piece.WHITE else sqr.piece.type.lower()
                else:
                    empty += 1
            if empty > 0:
                fen += str(empty)
            if i != 7:
                fen += "/"
        fen += " "
        # Turn
        fen += self.turn + " "

        fen += "KQkq - 0 1"

        return fen

    def place_piece(self, pos: Vec2, type_: str, color: str) -> None:
        self.board[pos.x, pos.y].piece = create_piece(type_)(Vec2(pos.x, pos.y), color)
        self.piece_positions[Piece.opposite_color(color)].discard(pos)
        self.piece_positions[color].add(pos)

    def remove_piece(self, pos: Vec2) -> None:
        """
        Removes a piece from the board
        :param pos: Vec2 containing the coords of the piece to remove
        :return: None
        """
        sqr: Square = self.board[pos.x, pos.y]
        if sqr.has_piece():
            self.piece_positions[sqr.piece.color].discard(pos)
            sqr.piece = None

    @staticmethod
    def valid_coords(coords: Vec2) -> bool:
        """
        Checks whether the given coordinates are within bounds
        :param coords: Vec2(grid X coordinate, grid Y coordinate)
        :return: bool
        """
        return 0 <= coords.x <= 7 and 0 <= coords.y <= 7

    @staticmethod
    def get_square_color(coords: Vec2) -> Piece.Color:
        return Piece.WHITE if (coords.x + coords.y) % 2 == 0 else Piece.BLACK

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
            self.selected_square.piece.compute_valid_moves(self.board)

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

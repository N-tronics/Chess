# PyGame interface
# Nischay Bharadwaj (N-tronics)

import pygame
import os
import game
from sys import exit as sys_exit
from pieces import *
from vector import *
from typing import *

pieces: List[str] = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']


class Chess:
    def __init__(self):
        # Pygame init
        self.WIN_DIMENS = Vec2(600, 600)
        self.WIN = pygame.display.set_mode(self.WIN_DIMENS.get_tuple())
        pygame.display.set_caption("Chess")
        self.FPS = 30
        self.clock = pygame.time.Clock()

        # Draw occurs only if this flag is set
        self.update_screen = True

        # Game control constants
        self.grid_offset = Vec2(21, 8)
        self.cell_size = Vec2(71.5, 71)
        self.grid_dimens = self.cell_size * Vec2(8, 8)
        self.board = game.ChessBoard()

        # Loading and scale images
        self.board_img = pygame.transform.scale(
            pygame.image.load(os.path.join(os.getcwd(), "images", "chess-board.png")),
            self.WIN_DIMENS.get_tuple()
        )
        self.piece_imgs: Dict[PieceColor, Dict[PieceType, pygame.Surface]] = {
            Piece.WTE: {piece_type: pygame.transform.scale(
                pygame.image.load(os.path.join(os.getcwd(), "images", f"w{Piece.get_name(piece_type)}.png")),
                self.cell_size.get_tuple()
            ) for piece_type in set(game.power_pieces + [Piece.PWN])},
            Piece.BLK: {piece_type: pygame.transform.scale(
                pygame.image.load(os.path.join(os.getcwd(), "images", f"b{Piece.get_name(piece_type)}.png")),
                self.cell_size.get_tuple()
            ) for piece_type in set(game.power_pieces + [Piece.PWN])}
        }

    def window_coords_to_grid_coords(self, w_coords: Vec2) -> Vec2 | None:
        """
        Converts window coordinates to grid coordinates
        :param w_coords: Vec2(x: window X coordinate, y: window Y coordinate)
        :return: Vec2(x: grid X coordinate, y: grid Y coordinate)
        """
        w_coords -= self.grid_offset
        if 0 <= w_coords.x <= self.grid_dimens.x and 0 <= w_coords.y <= self.grid_dimens.y:
            return Vec2(
                int(w_coords.x / self.cell_size.x),
                int(w_coords.y // self.cell_size.y)
            )

    def grid_coords_to_window_coords(self, g_coords: Vec2) -> Vec2:
        """
        Converts grid coordinates to window coordinates
        :param g_coords: Vec2(grid X coordinate, grid Y coordinate)
        :return: Vec2(window X coordinate, window Y coordinate)
        """
        return Vec2(
            self.grid_offset.x + self.cell_size.x * g_coords.x,
            self.grid_offset.y + self.cell_size.y * g_coords.y
        )

    def draw(self) -> None:
        """
        Draws and updates the screen only if needed
        :return: None
        """
        # Ensure that the update_screen flag is set
        # Even though this method gets called every frame,
        # A draw happens only if needed
        if not self.update_screen:
            return
        self.update_screen = False
        self.WIN.blit(self.board_img, (0, 0))

        # Draws grid lines
        # for i in range(9):
        #     pygame.draw.line(self.WIN, (255, 0, 0),
        #           (self.grid_offset.x + self.cell_size.x * i, self.grid_offset.y),
        #           (self.grid_offset.x + self.cell_size.x * i, self.grid_offset.y + self.cell_size.y * 8),
        #           1
        #     )
        # for i in range(9):
        #     pygame.draw.line(self.WIN, (255, 0, 0),
        #           (self.grid_offset.x, self.grid_offset.y + self.cell_size.y * i),
        #           (self.grid_offset.x + self.cell_size.x * 8, self.grid_offset.y + self.cell_size.y * i),
        #           1
        #     )

        if self.board.selected_square is not None:
            sel_sqr = pygame.Surface(self.cell_size.get_tuple(), pygame.SRCALPHA)
            sel_sqr.fill((255, 65, 0, 127))
            self.WIN.blit(sel_sqr, self.grid_coords_to_window_coords(self.board.selected_square.pos).get_tuple())

        for _, piece_positions in self.board.piece_positions.items():
            for g_coords in piece_positions:
                piece: Piece = self.board.board[g_coords.x, g_coords.y].piece
                coords: Vec2 = self.grid_coords_to_window_coords(piece.pos)
                self.WIN.blit(self.piece_imgs[piece.color][piece.type], coords.get_tuple())

        pygame.display.update()

    def start(self):
        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys_exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    g_coords: Vec2 = self.window_coords_to_grid_coords(Vec2(*pygame.mouse.get_pos()))
                    if g_coords:
                        self.update_screen = True
                        self.board.handle_click(g_coords)

            self.draw()


if __name__ == "__main__":
    chess = Chess()
    chess.start()

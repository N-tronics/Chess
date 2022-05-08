# FEN Generator
# Nischay Bharadwaj (N-tronics)

import pygame
import game
from main import Chess
from sys import exit as sys_exit
from game_constants import Piece
from vector import *
from typing import *


class FENGenerator:
    def __init__(self):
        self.chess = Chess()
        pygame.display.set_caption("FEN Generator")
        self.board = self.chess.board
        self.board.load_fen(game.empty_fen)
        self.piece_type = Piece.KING

    def start(self):
        while True:
            self.chess.clock.tick(self.chess.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys_exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed: Tuple[bool, bool, bool] = pygame.mouse.get_pressed()
                    g_coords: Vec2 = self.chess.window_coords_to_grid_coords(Vec2(*pygame.mouse.get_pos()))
                    if g_coords:
                        self.chess.update_screen = True
                        if pressed[0]:
                            self.board.place_piece(g_coords, self.piece_type, Piece.WHITE)
                        elif pressed[2]:
                            self.board.place_piece(g_coords, self.piece_type, Piece.BLACK)
                        elif pressed[1] and self.board.board[g_coords.x, g_coords.y].has_piece():
                            self.board.remove_piece(g_coords)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_k:
                        self.piece_type = Piece.KING
                    elif event.key == pygame.K_q:
                        self.piece_type = Piece.QUEEN
                    elif event.key == pygame.K_r:
                        self.piece_type = Piece.ROOK
                    elif event.key == pygame.K_b:
                        self.piece_type = Piece.BISHOP
                    elif event.key == pygame.K_n:
                        self.piece_type = Piece.KNIGHT
                    elif event.key == pygame.K_p:
                        self.piece_type = Piece.PAWN
                    elif event.key == pygame.K_RETURN:
                        print(self.board.generate_fen())
                    elif event.key == pygame.K_ESCAPE:
                        self.board.clear_board()
                        self.chess.update_screen = True

            self.chess.draw()


if __name__ == "__main__":
    print("KEY MAP:")
    print("k: KING")
    print("q: QUEEN")
    print("r: ROOK")
    print("b: BISHOP")
    print("n: KNIGHT")
    print("p: PAWN\n")
    print("left click: WHITE")
    print("right click: BLACK")
    print("middle click: delete piece")
    print("return: generate FEN\n")
    feng = FENGenerator()
    feng.start()

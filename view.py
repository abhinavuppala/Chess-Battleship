import pygame
import chess

BLACK, WHITE = pygame.color.Color(180, 180, 180), pygame.color.Color(255, 255, 255)
HIGHLIGHT_BLACK, HIGHLIGHT_WHITE = pygame.color.Color(182, 208, 226), pygame.color.Color(162, 188, 206)
HIGHLIGHT_SELECT = pygame.color.Color(31, 81, 255)
WHITE_TURN, BLACK_TURN = 0, 1

PIECE_SIZE = 75     # piece pixel size
ICON_SIZE = 30      # piece pixel size (when showing captured pieces)

class GameBoard:
    def __init__(self, surface: pygame.Surface, board: chess.Board):
        self.turn = WHITE_TURN
        self.surface = surface
        self.board = board
        self.sprite_dir = 'chess_sprites'

        # each piece to its corresponding image file name
        self.piece_to_number_map = {'p': '105', 'r': '104', 'n': '103', 'b': '102', 'q': '101', 'k': '100',
                               'P': '005', 'R': '004', 'N': '003', 'B': '002', 'Q': '001', 'K': '000'}

    def get_rect_from_gamepoint(self, gp: tuple[int, int]) -> pygame.Rect:
        """
        Given (r, c), return a square for the area on the game board
        """
        
        # get rect size, and corner x & y
        w, h = self.surface.get_size()
        r_size = min(w, h) / 8
        x, y = map(lambda x: x * r_size, gp)

        # return rectangle
        return pygame.Rect(x, y, r_size, r_size)
        

    def draw_blank_board(self) -> None:
        """
        Draw chess board with no pieces, just black & white squares
        """

        # initially fill with white, add in black squares after
        self.surface.fill(WHITE)

        for r in range(8):
            for c in range(8):
                if (r + c) % 2 == 0: continue   # white squares

                rect = self.get_rect_from_gamepoint((r, c))    # black squares
                pygame.draw.rect(
                    surface=self.surface, color=BLACK, rect=rect
                )

    def draw_highlighted_squares(self, squares: list[tuple[int, int]]) -> None:
        """
        Highlight all cells in the given list of squares
        """
        for r, c in squares:
            rect = self.get_rect_from_gamepoint((c, r))
            color = HIGHLIGHT_BLACK if (r + c) % 2 == 0 else HIGHLIGHT_WHITE
            pygame.draw.rect(
                surface=self.surface, color=color, rect=rect
            )

    def draw_selected_square(self, square: tuple[int, int]) -> None:
        """
        Highlight selected square
        """
        if square is None: return
        r, c = square
        rect = self.get_rect_from_gamepoint((c, r))
        pygame.draw.rect(
            surface=self.surface, color=HIGHLIGHT_SELECT, rect=rect
        )

    def draw_pieces(self, turn: int) -> None:
        """
        Draw pieces from the string representation of the game board
        """
        # split board into grid of characters
        board_str = str(self.board)
        board_grid = [board_str[16*i : 16*i + 15].split() for i in range(8)]

        # hide opposing pieces based on whose turn it is
        self.hide_opposing_pieces(board_grid, turn)
        
        # for each non-empty square, draw the corresponding piece
        for r in range(8):
            for c in range(8):
                if board_grid[r][c] == '.': continue
                self.draw_piece(self.piece_to_number_map[board_grid[r][c]], r, c)


    def draw_piece(self, filename: str, r: int, c: int) -> None:
        """
        Draw 1 piece from the given file number (string)
        """
        y, x = self.get_rect_from_gamepoint((r, c)).topleft     # get top-left coordinate of piece

        # load PNG image, scale it to 75x75, and draw it onto surface at given coords
        image = pygame.image.load(f'{self.sprite_dir}/tile{filename}.png').convert_alpha()
        image = pygame.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))
        self.surface.blit(image, (x, y))


    def draw_captured_pieces(self) -> None:
        """
        Displays all the captured pieces on the bottom of the board
        """
        pieces = self.captured_pieces()
        left = False
        lc, rc = 0, 0
        
        for p in pieces:
            if p.isupper(): left = True     # white piece

            # load PNG image, scale it to 20x20, draw it onto the bottom
            filenum = self.piece_to_number_map[p]
            image = pygame.image.load(f'{self.sprite_dir}/tile{filenum}.png').convert_alpha()
            image = pygame.transform.scale(image, (ICON_SIZE, ICON_SIZE))

            # places the pieces so that they fill up at most 2 lines
            # along with seperating black & white pieces into left/right
            if left:
                if lc >= 8:
                    self.surface.blit(image, ((1 + lc - 8) * ICON_SIZE, 650))
                else:    
                    self.surface.blit(image, ((1 + lc) * ICON_SIZE, 620))
                lc += 1
            else:
                if rc >= 8:
                    self.surface.blit(image, ((1 + rc - 8) * ICON_SIZE + 4 * PIECE_SIZE, 650))
                else:    
                    self.surface.blit(image, ((1 + rc) * ICON_SIZE + 4 * PIECE_SIZE, 620))
                rc += 1


    def display_next_move_text(self) -> None:
        """
        Display text saying press space to move to next turn
        """
        w, h = self.surface.get_size()
        font = pygame.font.SysFont('Comic Sans MS', 40)
        
        # centers the text by finding text dimensions relative to surface
        text_surface = font.render('Press SPACE to finish turn', False, pygame.color.Color(255, 0, 0))
        tw, th = font.size('Press SPACE to finish turn')
        self.surface.blit(text_surface, (0.5 * (w - tw), 0.5 * (h - th)))


    def hide_opposing_pieces(self, board_grid: list[list[str]], turn: int) -> None:
        """
        Modifies board_grid in-place, removes all pieces of opposing side
        """
        # condition by which to remove pieces (lowercase => remove white, etc.)
        condition = (lambda s: s.isupper()) if turn == 1 else (lambda s: s.islower())
        for r in range(8):
            for c in range(8):
                if condition(board_grid[r][c]):
                    board_grid[r][c] = '.'


    def game_over(self) -> None:
        """
        Returns true if the game is over (no legal moves can be made)
        """
        return len([*self.board.legal_moves]) == 0
    

    def captured_pieces(self) -> str:
        """
        Gets all pieces that have been captured (not on the game board)
        """
        # get all pieces & pieces currently on board
        current_pieces = str(self.board).replace('.', '').replace(' ', '').replace('\n', '')
        all_pieces = 'rnbqkbnrppppppppPPPPPPPPRNBQKBNR'
        
        # note: lowercase is black, uppercase is white
        missing_pieces = ''
        for c in 'rnbqkpRNBQKP':
            missing_pieces += c * (all_pieces.count(c) - current_pieces.count(c))

        return missing_pieces
    

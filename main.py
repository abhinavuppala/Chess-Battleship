import chess
from collections import defaultdict
from view import *

FRAMERATE = 30

def run() -> None:
    """
    Runs the full chess game
    """
    highlighted_moves = []
    selected_piece = None
    turn = WHITE_TURN

    def handle_click(pos: tuple[int, int]) -> None:
        """
        Selects a piece or moves the selected piece to the spot
        """
        nonlocal selected_piece
        nonlocal highlighted_moves
        nonlocal turn
        c, r = map(lambda x: x // PIECE_SIZE, pos)

        # deselect piece if selected
        if selected_piece == (r, c):
            selected_piece = None
            highlighted_moves = []

        # move to selected piece, since it is a legal move
        # await a space key press to indicate next person's turn
        elif (r, c) in highlighted_moves:
            start, end = cell_to_str(selected_piece), cell_to_str((r, c))
            board.push_san(start + end)
            selected_piece = None
            highlighted_moves = []

            # show text prompting to press SPACE
            # while hiding the move so other player doesn't see
            surface.fill(WHITE)
            gb.display_next_move_text()
            pygame.display.flip()

            # wait until space is pressed to confirm move (or check for quit)
            space_pressed = False
            while not space_pressed:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    exit()
                if event.type == 769:   # space key up
                    turn = (turn + 1) % 2   # update turn
                    print(f"{'WHITE' if turn == WHITE_TURN else 'BLACK'}'s turn!")
                    space_pressed = True


        # get row & column of legal moves from this position
        else:
            selected_piece = (r, c)
            highlighted_moves = get_move_dict(board)[(r, c)]
 
    # initializing pygame, chess & GameBoard variables
    surface = pygame.display.set_mode((8 * PIECE_SIZE, 8 * PIECE_SIZE + 150))
    board = chess.Board()
    gb = GameBoard(surface, board)

    clock = pygame.time.Clock()
    pygame.font.init()
    pygame.display.set_caption('Chess?')
    running = True

    while running:
        clock.tick(FRAMERATE)

        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                running = False

            # left click event - move/select piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                handle_click(pos)
            
        # draw board, highlighs, and pieces along with showing captured pieces
        gb.draw_blank_board()
        gb.draw_highlighted_squares(highlighted_moves)
        gb.draw_selected_square(selected_piece)
        gb.draw_pieces(turn)
        gb.draw_captured_pieces()

        # if game over, display text
        if gb.game_over():
            display_game_over(surface)

        pygame.display.flip()


def str_to_cell(s: str) -> tuple[int, int]:
    """
    Given notation like e4, converts to a row/col pair
    """
    col, row = s[0], int(s[1])
    col = "abcdefgh".index(col)
    row = 8 - row
    return (row, col)


def cell_to_str(cell: tuple[int, int]) -> str:
    """
    Given a game board cell like (r, c), converts to chess notation like e4
    """
    r, c = cell
    letter = "abcdefgh"[c]
    number = str(8 - r)
    return letter + number


def get_move_dict(board: chess.Board) -> defaultdict[tuple, list[tuple]]:
    """
    Given a board, returns all possible legal moves (accounts for turn)
    """
    moves = defaultdict(lambda: [])     # stores like so - (start): [(end1), (end2), ...]
    for move in board.legal_moves:
        start, end = str_to_cell(str(move)[:2]), str_to_cell(str(move)[2:])
        moves[start].append(end)        # converts each move from SAN format to points (tuples) and saves
    return moves


def display_game_over(surface: pygame.Surface) -> None:
    """
    Displays game over text on the screen
    """
    w, h = surface.get_size()
    font = pygame.font.SysFont('Comic Sans MS', 40)
    
    # centers the text by finding text dimensions relative to surface
    text_surface = font.render('Game Over!', False, pygame.color.Color(255, 0, 0))
    tw, th = font.size('Game Over!')
    surface.blit(text_surface, (0.5 * (w - tw), 0.5 * (h - th)))


if __name__ == '__main__':
    run()
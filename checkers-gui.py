import enum
import sys
import pygame
import nbimporter
from Checkers_backup import Checkers
from pygame.rect import Rect
import pygame.gfxdraw
import chess

pygame.init()

SQUARE_SIZE = 50
BOARD_SIZE = 8

screen_width = BOARD_SIZE * SQUARE_SIZE
screen_height = BOARD_SIZE * SQUARE_SIZE

screen_size = (screen_width, screen_height)

screen = pygame.display.set_mode(screen_size)


DEFAULT_BOARD = chess.Board("1p1p1p1p/p1p1p1p1/1p1p1p1p/8/8/P1P1P1P1/1P1P1P1P/P1P1P1P1 b KQkq - 0 4")


class Color(enum.Enum):
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)


BLACK_KING = pygame.transform.scale(
    pygame.image.load('checkers-assets/black_king.png'),
    (SQUARE_SIZE, SQUARE_SIZE))

BLACK_NORMAL = pygame.transform.scale(
    pygame.image.load('checkers-assets/black_normal.png'),
    (SQUARE_SIZE, SQUARE_SIZE))

WHITE_KING = pygame.transform.scale(
    pygame.image.load('checkers-assets/white_king.png'),
    (SQUARE_SIZE, SQUARE_SIZE))

WHITE_NORMAL = pygame.transform.scale(
    pygame.image.load('checkers-assets/white_normal.png'),
    (SQUARE_SIZE, SQUARE_SIZE))

HIGHLIGHT_COLOR = pygame.Color(255, 0, 0)


def is_game_over():
    return False


def get_piece_image(piece):
    if piece.piece_type is chess.PAWN:
        if piece.color is chess.WHITE:
            return WHITE_NORMAL
        else:
            return BLACK_NORMAL
    else:
        if piece.color is chess.WHITE:
            return WHITE_KING
        else:
            return BLACK_KING


def get_top_left(i, j):
    return (BOARD_SIZE - i - 1) * SQUARE_SIZE, j * SQUARE_SIZE


def draw_piece(i, j, piece):
    piece_image = get_piece_image(piece)
    top, left = get_top_left(i, j)
    screen.blit(piece_image, (left, top))


def get_coordinates(square):
    return square // BOARD_SIZE, square % BOARD_SIZE


def draw_pieces(board):
    for square, piece in board.piece_map().items():
        i, j = get_coordinates(square)
        draw_piece(i, j, piece)


def draw_board(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            draw_square(i, j)

    draw_pieces(board)


def draw_square(i, j):
    top, left = get_top_left(i, j)
    square = pygame.rect.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)
    pygame.gfxdraw.box(screen, square, get_color(i, j))


def get_color(i, j):
    if (i + j) % 2:
        return pygame.Color(232, 235, 239)
    return pygame.Color(125, 135, 150)


def get_square_from_coordinates(x, y):
    return x * BOARD_SIZE + y


def get_clicked_square(clicked_position):
    x, y = clicked_position
    x, y = screen_height - y, x
    square_i, square_j = x // SQUARE_SIZE, y // SQUARE_SIZE
    return get_square_from_coordinates(square_i, square_j)


def attempt_move(checkers, from_square, to_square):
    checkers.move_or_ignore(from_square, to_square)


def highlight_square(square_clicked):
    x, y = get_coordinates(square_clicked)
    top, left = get_top_left(x, y)
    highlighting_rectangle = pygame.rect.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)
    pygame.gfxdraw.rectangle(screen, highlighting_rectangle, HIGHLIGHT_COLOR)


def perform_click_operation(checkers, clicked_position, square_selected):
    square_clicked = get_clicked_square(clicked_position)

    if not square_selected:
        return square_clicked

    if square_clicked is not square_selected:
        attempt_move(checkers, square_selected, square_clicked)

    return None


def game():
    clicked_position = None
    square_selected = None
    checkers = Checkers()

    while not is_game_over():
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                sys.exit()
            elif event.type is pygame.MOUSEBUTTONUP:
                clicked_position = pygame.mouse.get_pos()

        if clicked_position:
            square_selected = perform_click_operation(checkers, clicked_position, square_selected)
            clicked_position = None

        else:
            checkers.attempt_bot_move()

        draw_and_update(checkers, square_selected)


def draw_and_update(checkers, square_selected):
    draw_board(checkers.board)
    if square_selected:
        highlight_square(square_selected)
    pygame.display.update()


def simulate_bot_vs_bot():
    checkers = Checkers()

    while True:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                sys.exit()

        draw_and_update(checkers, None)

        checkers.make_bot_move_any_color()


if __name__ == '__main__':
    # game()
    simulate_bot_vs_bot()

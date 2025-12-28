import time
import random
from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY

# --- Hardware setup ---
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=270)
display.set_backlight(0.6)

button_a = Button(12)  # rotate
button_b = Button(13)  # soft drop
button_x = Button(14)  # left
button_y = Button(15)  # right

led = RGBLED(6, 7, 8)

# --- Game constants ---
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

CELL_SIZE = 10

BOARD_PIX_W = BOARD_WIDTH * CELL_SIZE
BOARD_PIX_H = BOARD_HEIGHT * CELL_SIZE

# After rotate=270, the screen is 135x240
SCREEN_W = 135
SCREEN_H = 240

OFFSET_X = (SCREEN_W - BOARD_PIX_W) // 2
OFFSET_Y = (SCREEN_H - BOARD_PIX_H) // 2

BG_COLOR = (0, 0, 0)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)

# Tetrimino shapes: each is list of rotation states, each state = list of (x, y) cells
TETROMINOS = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "L": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "J": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
    ],
}

COLORS = {
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "T": (180, 0, 255),
    "L": (255, 165, 0),
    "J": (0, 0, 255),
    "S": (0, 255, 0),
    "Z": (255, 0, 0),
}

# --- Game state ---
board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

current_piece = None
current_shape = None
current_rot = 0
current_x = 3
current_y = 0

score = 0
game_over = False

last_fall_time = time.ticks_ms()
FALL_INTERVAL = 600  # ms


def new_piece():
    global current_piece, current_shape, current_rot, current_x, current_y
    current_piece = random.choice(list(TETROMINOS.keys()))
    current_shape = TETROMINOS[current_piece]
    current_rot = 0
    current_x = 3
    current_y = 0


def get_cells(piece, shape, rot, px, py):
    cells = []
    for (dx, dy) in shape[rot]:
        x = px + dx
        y = py + dy
        cells.append((x, y))
    return cells


def valid_position(px, py, rot):
    cells = get_cells(current_piece, current_shape, rot, px, py)
    for (x, y) in cells:
        if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
            return False
        if board[y][x] is not None:
            return False
    return True


def lock_piece():
    global board
    cells = get_cells(current_piece, current_shape, current_rot, current_x, current_y)
    color = COLORS[current_piece]
    for (x, y) in cells:
        if 0 <= y < BOARD_HEIGHT:
            board[y][x] = color


def clear_lines():
    global board, score
    new_board = []
    cleared = 0
    for row in board:
        if all(cell is not None for cell in row):
            cleared += 1
        else:
            new_board.append(row)
    while len(new_board) < BOARD_HEIGHT:
        new_board.insert(0, [None for _ in range(BOARD_WIDTH)])
    board = new_board
    if cleared > 0:
        score += cleared * 100
    return cleared


def reset_game():
    global board, score, game_over
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            board[y][x] = None
    score = 0
    game_over = False
    new_piece()


def clear_screen():
    r, g, b = BG_COLOR
    display.set_pen(display.create_pen(r, g, b))
    display.clear()


def draw_board():
    # grid
    r, g, b = GRID_COLOR
    grid_pen = display.create_pen(r, g, b)
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            rx = OFFSET_X + x * CELL_SIZE
            ry = OFFSET_Y + y * CELL_SIZE
            display.set_pen(grid_pen)
            display.rectangle(rx, ry, CELL_SIZE - 1, CELL_SIZE - 1)
            cell = board[y][x]
            if cell is not None:
                cr, cg, cb = cell
                display.set_pen(display.create_pen(cr, cg, cb))
                display.rectangle(rx + 1, ry + 1, CELL_SIZE - 3, CELL_SIZE - 3)


def draw_current_piece():
    cells = get_cells(current_piece, current_shape, current_rot, current_x, current_y)
    cr, cg, cb = COLORS[current_piece]
    pen = display.create_pen(cr, cg, cb)
    for (x, y) in cells:
        if y < 0:
            continue
        rx = OFFSET_X + x * CELL_SIZE
        ry = OFFSET_Y + y * CELL_SIZE
        display.set_pen(pen)
        display.rectangle(rx + 1, ry + 1, CELL_SIZE - 3, CELL_SIZE - 3)


def draw_ui():
    # score
    r, g, b = TEXT_COLOR
    display.set_pen(display.create_pen(r, g, b))
    display.text(str(score), OFFSET_X, OFFSET_Y - 20, scale=2)
    if game_over:
        display.text("GAME OVER", OFFSET_X + 10, OFFSET_Y + 40, scale=2)
        display.text("A=Restart", OFFSET_X + 10, OFFSET_Y + 60, scale=2)


def update_led():
    if game_over:
        led.set_rgb(255, 0, 0)
    else:
        led.set_rgb(0, 40, 0)


def handle_input():
    global current_x, current_y, current_rot, game_over

    if game_over:
        # press A to restart
        if button_a.read():
            reset_game()
        return

    moved = False

    # left / right
    if button_x.read():
        if valid_position(current_x + 1, current_y, current_rot):
            current_x += 1
            moved = True

    if button_y.read():
        if valid_position(current_x - 1, current_y, current_rot):
            current_x -= 1
            moved = True

    # rotate
    if button_a.read():
        new_rot = (current_rot + 1) % len(current_shape)
        if valid_position(current_x, current_y, new_rot):
            current_rot = new_rot
            moved = True

    # soft drop
    if button_b.read():
        if valid_position(current_x, current_y + 1, current_rot):
            current_y += 1
            moved = True

    if moved:
        # simple debounce
        time.sleep(0.1)


def get_ghost_y():
    gy = current_y
    while valid_position(current_x, gy + 1, current_rot):
        gy += 1
    return gy


def draw_ghost_piece():
    gy = get_ghost_y()
    cells = get_cells(current_piece, current_shape, current_rot, current_x, gy)
    ghost_pen = display.create_pen(255, 255, 255)

    for (x, y) in cells:
        if y < 0:
            continue
        rx = OFFSET_X + x * CELL_SIZE
        ry = OFFSET_Y + y * CELL_SIZE
        display.set_pen(ghost_pen)
        display.rectangle(rx + 1, ry + 1, CELL_SIZE - 3, CELL_SIZE - 3)


def main():
    global current_y, last_fall_time, game_over

    reset_game()
    new_piece()

    while True:
        now = time.ticks_ms()

        handle_input()

        if not game_over and time.ticks_diff(now, last_fall_time) >= FALL_INTERVAL:
            last_fall_time = now
            if valid_position(current_x, current_y + 1, current_rot):
                current_y += 1
            else:
                lock_piece()
                lines = clear_lines()
                new_piece()
                if not valid_position(current_x, current_y, current_rot):
                    game_over = True

        clear_screen()
        draw_board()
        if not game_over:
            draw_ghost_piece()
            draw_current_piece()
        draw_ui()
        update_led()
        display.update()

        time.sleep(0.02)


main()

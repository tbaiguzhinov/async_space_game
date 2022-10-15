import asyncio
import curses
import random
from itertools import cycle

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258
BORDER_WIDTH = 2


async def blink(canvas, row, column, offset_tics, symbol='*'):
    """Display animation of a star with various blinking speed."""
    while True:
        for index, offset_tic in enumerate(offset_tics):
            if index == 0:
                canvas.addstr(row, column, symbol, curses.A_DIM)
            elif index == 2:
                canvas.addstr(row, column, symbol, curses.A_BOLD)
            else:
                canvas.addstr(row, column, symbol)
            for _ in range(offset_tic):
                await asyncio.sleep(0)


def get_random_star_params(row, column):
    """Get a random star symbol with random row and column."""
    star_symbols = '+*.:'
    return random.randint(BORDER_WIDTH, row-BORDER_WIDTH), \
        random.randint(BORDER_WIDTH, column-BORDER_WIDTH), \
        random.choice(star_symbols)


async def fire(
        canvas,
        start_row,
        start_column,
        rows_speed=-0.3,
        columns_speed=0
):
    """Display animation of gun shot, direction and speed can be specified."""
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def draw_frame(canvas, start_row, start_column, frame, negative=False):
    """Draw multiline frame fragment on canvas.

    Erase frame instead of drawing if negative=True is specified.
    """
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(frame.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position is not in a lower right corner
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(frame):
    """Calculate size of multiline text fragment.

    Return pair — number of rows and colums.
    """
    lines = frame.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


async def animate_spaceship(canvas, frames, window_rows, window_columns):
    row = window_rows / 2
    column = window_columns / 2
    for frame in cycle(frames):
        height, width = get_frame_size(frame)
        row_limit = window_rows - height
        column_limit = window_columns - width
        for _ in range(4):
            rows_direction, columns_direction, space = read_controls(canvas)
            next_row = row + rows_direction
            next_column = column + columns_direction
            if 0 < next_row < row_limit:
                row = next_row
            if 0 < next_column < column_limit:
                column = next_column
            draw_frame(canvas, row, column, frame, negative=False)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed

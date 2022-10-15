import curses
import time
import random

from animations import animate_spaceship, blink, fire, get_random_star_params

TIC_TIMEOUT = 0.1


def draw(canvas):
    frames = []
    for frame in range(1, 3):
        with open(f'animation_sprites/rocket_frame_{frame}.txt', 'r') as file:
            frames.append(file.read())

    curses.curs_set(False)
    canvas.border()
    row_window, column_window = curses.window.getmaxyx(canvas)

    coroutines = []
    for _ in range(200):
        row, column, symbol = get_random_star_params(row_window, column_window)
        offset_tics = [random.randint(1, offset) for offset in [20, 3, 5, 3]]
        coroutine = blink(canvas, row, column, offset_tics, symbol)
        coroutines.append(coroutine)
    coroutines.append(
        fire(canvas, start_row=row_window-2, start_column=column_window/2)
    )
    coroutines.append(
        animate_spaceship(canvas, frames=frames,
                          row_window=row_window, column_window=column_window),
    )

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    window = curses.initscr()
    window.nodelay(True)
    curses.wrapper(draw)


if __name__ == '__main__':
    main()

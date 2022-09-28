import curses
import time

from animations import animate_spaceship, blink, fire, get_star

TIC_TIMEOUT = 0.1


def draw(canvas):
    texts = []
    for number in range(1, 3):
        with open(f'animation_images/rocket_frame_{number}.txt', 'r') as file:
            texts.append(file.read())

    curses.curs_set(False)
    canvas.border()
    row_window, column_window = curses.window.getmaxyx(canvas)

    coroutines = []
    for _ in range(200):
        row, column, symbol = get_star(row_window, column_window)
        coroutine = blink(canvas, row, column, symbol)
        coroutines.append(coroutine)
    coroutines.append(
        fire(canvas, start_row=row_window-2, start_column=column_window/2)
    )
    coroutines.append(
        animate_spaceship(canvas, texts=texts,
                          row_window=row_window, column_window=column_window),
    )

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    window = curses.initscr()
    window.nodelay(True)
    curses.wrapper(draw)


if __name__ == '__main__':
    main()

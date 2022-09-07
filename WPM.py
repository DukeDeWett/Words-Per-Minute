import random
import time
import curses
from curses import wrapper


def start(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome! Let us see how fast do you write!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()


def display(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_count(stdscr):
    target_text = load_text()
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_passed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_passed / 60)) / 5)

        stdscr.clear()
        display(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except (Exception,):
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start(stdscr)
    while True:
        wpm_count(stdscr)
        stdscr.addstr(2, 0, "You finished the game! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)

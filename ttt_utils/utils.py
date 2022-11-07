"""
Utility functions for general housekeeping.
check_platform: Exits if not a supported platform; adjust Windows scale.
manage_args: Handles command line arguments.
program_name:
quit_gui: Safe and informative exit from the program.
"""
# Copyright (C) 2021-2022 C.S. Echt under MIT License'

# Standard library imports:
import argparse
import logging
import platform
import sys
# Local program imports:
from pathlib import Path
from __main__ import __doc__
from ttt_utils import (__author__,
                       __copyright__,
                       __dev_status__,
                       __license__,
                       __version__,
                       URL)
from ttt_utils.constants import (MY_OS,
                                 KP2PLAY,
                                 KEYS2PLAY)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Changes an unhandled exception to go to stdout rather than
    stderr. Ignores KeyboardInterrupt so a console program can exit
    with Ctrl + C. Relies entirely on python's logging module for
    formatting the exception. Source:
    https://stackoverflow.com/questions/6234405/
    logging-uncaught-exceptions-in-python/16993115#16993115
    https://stackoverflow.com/questions/43941276/
    python-tkinter-and-imported-classes-logging-uncaught-exceptions/
    44004413#44004413

    Usage: in mainloop,
     - sys.excepthook = utils.handle_exception
     - app.report_callback_exception = utils.handle_exception

    :param exc_type:
    :param exc_value:
    :param exc_traceback:
    :return: None
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def check_platform():
    if MY_OS not in 'lin, win, dar':
        print(f'Platform <{sys.platform}> is not supported.\n'
              'Windows, Linux, and MacOS (darwin) are supported.')
        sys.exit(1)

    # Need to account for scaling in Windows10 and earlier releases.
    if MY_OS == 'win':
        from ctypes import windll

        if platform.release() < '10':
            windll.user32.SetProcessDPIAware()
        else:
            windll.shcore.SetProcessDpiAwareness(1)


def keybindings(parent, state: str) -> None:
    """
    Key bindings for quit function and to play game board squares.

    Provides alternative play action to mouse clicks.
    Can use both key commands and the mouse when two people are
    playing Player v Player mode.

    :param parent: The parent tk widget or mainloop to bind to.
    :param state: Either 'quit_keys', 'bind_board' or 'unbind_board'.
    :return: None
    """

    # KP2PLAY and  KEYS2PLAY are strings of keys corresponding to a
    #   positional 3x3 layout on the keypad and main board. Character
    #   order of each string corresponds with the 3x3 game board
    #   row-column layout and sorted board_label index values.
    # Note: '<Control-q>' will not be preempted by the 'q' binding
    #   when KeyRelease is used to bind the 'q' in KEYS2PLAY string.
    def bind2this(index):
        parent.human_turn(parent.board_labels[index])

    if state == 'quit_keys':
        parent.bind_all('<Control-q>',
                        lambda _: quit_game(parent))
        parent.bind_all('<Escape>',
                        lambda _: quit_game(parent))

    elif state == 'bind_board':
        for i, _n, in enumerate(KP2PLAY, start=0):
            parent.bind(f'<KeyPress-KP_{_n}>',
                        lambda _, indx=i: bind2this(indx))

        for i, _k, in enumerate(KEYS2PLAY, start=0):
            parent.bind(f'<KeyRelease-{_k}>',
                        lambda _, indx=i: bind2this(indx))
            # Include uppercase in case Caps Lock is on.
            parent.bind(f'<KeyRelease-{_k.upper()}>',
                        lambda _, indx=i: bind2this(indx))

    else:  # state is 'unbind_board'
        for _n in KP2PLAY:
            parent.unbind(f'<KeyPress-KP_{_n}>')

        for _k in KEYS2PLAY:
            parent.unbind(f'<KeyRelease-{_k}>')
            parent.unbind(f'<KeyRelease-{_k.upper()}>')


def manage_args() -> None:
    """Manage command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--about',
                        help='Provides description, version, URL, license',
                        action='store_true',
                        default=False)
    args = parser.parse_args()
    if args.about:
        print('====================== ABOUT START ====================')
        print(__doc__)
        print(f'{"Author:".ljust(13)}', __author__)
        print(f'{"Version:".ljust(13)}', __version__)
        print(f'{"Status:".ljust(13)}', __dev_status__)
        print(f'{"URL:".ljust(13)}', URL)
        print(__copyright__)
        print(__license__)
        print('====================== ABOUT END ====================')

        sys.exit(0)


def program_name() -> str:
    """
    Extract the main program's file name from the full path.

    Expected use is for printing and Terminal message display.

    :return: Name of the main script file.
    """
    return Path(sys.modules['__main__'].__file__).name


def quit_game(mainloop, keybind=None) -> None:
    """
    Error-free and informative exit from the program.

    Explicitly closes all Matplotlib objects and their parent tk window
    when the user closes the plot window with the system's built-in
    close window icon ("X") or key command. This is required to cleanly
    exit and close the tk thread running Matplotlib.
    Is called from widget or keybindings.

    :param mainloop: The main tk.Tk() window running the mainloop.
    :param keybind: Implicit event passed from bind().
    :return: None
    """

    print('\n*** User quit the program. ***\n')

    # pylint: disable=broad-except
    try:
        mainloop.update_idletasks()
        mainloop.after(200)
        mainloop.destroy()
    except Exception as err:
        print(f'An error occurred: {err}')
        sys.exit('Program exit with unexpected condition.')

    return keybind


def valid_path_to(relative_path: str) -> Path:
    """
    Get correct path to program's directory/file structure
    depending on whether program invocation is a standalone app or
    the command line. Works with symlinks. Allows command line
    using any path; does not need to be from parent directory.
    _MEIPASS var is used by distribution programs from
    PyInstaller --onefile; e.g. for images dir.

    :param relative_path: Program's local dir/file name, as string.
    :return: Absolute path as pathlib Path object.
    """
    # Modified from: https://stackoverflow.com/questions/7674790/
    #    bundling-data-files-with-pyinstaller-onefile and PyInstaller manual.
    if getattr(sys, 'frozen', False):  # hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', Path(Path(__file__).resolve()).parent)
        valid_path = Path(base_path) / relative_path
    else:
        valid_path = Path(Path(__file__).parent, f'../{relative_path}').resolve()
    return valid_path

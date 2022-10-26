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
import sys
import platform

from pathlib import Path

# Local program imports:
from __main__ import __doc__
import ttt_utils  # Needed for __init__.py custom dunders and constants.
from ttt_utils.constants import MY_OS, KP2PLAY, KEYS2PLAY


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
    :param state: Either 'quit', 'bind_board' or 'unbind_board'.
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
    """Allow handling of common command line arguments.
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
        print(f'{"Author:".ljust(13)}', ttt_utils.__author__)
        print(f'{"Version:".ljust(13)}', ttt_utils.__version__)
        print(f'{"Status:".ljust(13)}', ttt_utils.__dev_status__)
        print(f'{"URL:".ljust(13)}', ttt_utils.URL)
        print(ttt_utils.__copyright__)
        print(ttt_utils.__license__)
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

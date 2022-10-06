"""
Housekeeping functions:.
manage_args - Handles command line arguments.
quit_gui - Safe and informative exit from the program.
"""
# Copyright (C) 2021-2022 C.S. Echt under GNU General Public License'

# Standard library imports:
import argparse
import sys
from pathlib import Path

# Local program imports:
from __main__ import __doc__
import ttt_utils


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
    Called from widget or keybindings.
    Explicitly closes all Matplotlib objects and their parent tk window
    when the user closes the plot window with the system's built-in
    close window icon ("X") or key command. This is required to cleanly
    exit and close the tk thread running Matplotlib.

    :param mainloop: The main tk.Tk() window running the mainloop.
    :param keybind: Implicit event passed from bind().
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

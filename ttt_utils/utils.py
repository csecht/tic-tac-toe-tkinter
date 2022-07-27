import argparse
import sys
import __main__

import ttt_utils

# Copyright (C) 2021 C. Echt under GNU General Public License'


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
        print(__main__.__doc__)
        print(f'{"Author:".ljust(13)}', ttt_utils.__author__)
        print(f'{"Version:".ljust(13)}', ttt_utils.__version__)
        print(f'{"Status:".ljust(13)}', ttt_utils.__dev_status__)
        print(f'{"URL:".ljust(13)}', ttt_utils.URL)
        print(ttt_utils.__copyright__)
        print(ttt_utils.LICENSE)
        print('====================== ABOUT END ====================')

        sys.exit(0)


def quit_game(keybind=None) -> None:
    """
    Error-free and informative exit from the program.
    Called from widget or keybindings.
    Explicitly closes all Matplotlib objects and their parent tk window
    when the user closes the plot window with the system's built-in
    close window icon ("X") or key command. This is required to cleanly
    exit and close the tk thread running Matplotlib.

    :param keybind: Implicit event passed from bind().
    """

    print('\n*** User quit the program. ***\n')

    # pylint: disable=broad-except
    try:
        __main__.app.update_idletasks()
        __main__.app.after(200)
        __main__.app.destroy()
    except Exception as err:
        print(f'An error occurred: {err}')
        sys.exit('Program exit with unexpected condition.')

    return keybind

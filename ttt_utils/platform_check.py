"""
Check that a supported system platform is present.
Constants: MY_OS - abbreviated platform ID, used throughout main program.
Functions: check_platform - called from ttt_utils.__init__ at startup.
"""
# Copyright (C) 2021-2022 C.S. Echt under MIT License'

import sys
import platform

MY_OS = sys.platform[:3]


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

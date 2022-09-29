"""
Constants used by ttt.py.
PLAYER1, PLAYER2: the displayed player names.
P1_MARK, P2_MARK: 'X', 'O', respectively, but can be changed.
WINING_COMBOS: list of tuples.
PLAY_AFTER, AUTO_AFTER: ms integers for tk after() function.
"""
# Copyright (C) 2022 C.S. Echt under GNU General Public License'

# Used only for display of player ID.
PLAYER1 = 'PLAYER 1'
PLAYER2 = 'PLAYER 2'

# Can use any utf-8 character for play marks.
P1_MARK = 'X'
P2_MARK = 'O'

# Lists of tuples of winning board_labels and corner indices for board
#  squares (self.board_labels) used in ttt.py.
WINING_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),  # diagonals
]

CORNERS = [0, 2, 6, 8]

# Milliseconds for after(), pause between turns in play PC mode.
PLAY_AFTER = 600

# Milliseconds for after(), pause between autoplay turns and game turnovers.
AUTO_AFTER = 300

# Foreground and background colors.
COLOR = {'score_fg': 'DodgerBlue4',
         'result_bg': 'yellow3',
         'disabled_fg': 'grey65',
         'tk_white': '',  # defined in configure_widgets()
         'mark_fg': 'yellow2',
         'sq_won': 'blue',
         'sq_not_won': 'black',
         'sq_mouseover': 'grey15',
         'radiobtn_bg': 'DodgerBlue1',
         }

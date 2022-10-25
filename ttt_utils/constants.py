"""
Constants and configuration settings.
PLAYER1, PLAYER2: the displayed player names.
P1_MARK, P2_MARK: 'X', 'O', respectively, but can be changed.
MARKS1, MARKS2: strings of duplicate marks that determine number of auto turns.
WINNING_COMBOS, CORNERS, SIDES, PARA_CORNERS, ORTHO_SIDES, META_POSITIONS:
    lists of game board indices.
KP2PLAY, KEYS2PLAY: strings of ordered keys for bind() functions.
PLAY_AFTER, AUTO_FAST, AUTO_SLOW: ms integers for tk after() function.
TIES, WINS: (unused) tuples of board end-game configurations, in index order.
"""
# Copyright (C) 2022 C.S. Echt under MIT License'

from ttt_utils import platform_check  # need MY_OS

# Used only for display of player ID.
PLAYER1 = 'Player 1'
PLAYER2 = 'Player 2'

# Can use any utf-8 character for play marks.
P1_MARK = 'X'
P2_MARK = 'O'

# Set number of auto-player turns; used in auto_turns_limit().
MARKS1 = P1_MARK * 500
MARKS2 = P2_MARK * 500

# Keys in positional 3x3 layout on keypad and main board correspond
#   with the 3x3 game board row-column layout and sorted
#   board_labels index values.
KP2PLAY = '789456123'
KEYS2PLAY = 'qweasdzxc'

# 3x3 game board indices for winning combinations and corners.
WINNING_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),  # diagonals
]

CORNERS = [0, 2, 6, 8]
SIDES = [1, 3, 5, 7]
# ORTHO_CORNERS = ([0, 2], [0, 6], [2, 8], [6, 8])
PARA_CORNERS = ([0, 8], [2, 6])

# Dictionaries where key is index to be played in response to value for
#   an opponent's played indices.
# Keys are orthogonal (nearest) corner indices to opponent's played indices.
ORTHO_SIDES = {
    0: [1, 3],
    2: [1, 5],
    6: [3, 7],
    8: [5, 7]
}

META_POSITIONS = {
    0: [2, 3],
    2: [0, 5],
    6: [3, 8],
    8: [5, 6]
}

# Milliseconds, used in after() calls.
PLAY_AFTER = 600  # PC response time for PvPC mode.
AUTO_FAST = 100  # Fast cycle time for all autoplay modes.
AUTO_SLOW = 1000  # Slow cycle time for all autoplay modes.

# Foreground and background colors.
COLOR = {'score_fg': 'DodgerBlue4',
         'status_bg': 'yellow3',
         'disabled_fg': 'grey65',
         'tk_white': '',
         'mark_fg': 'yellow2',
         'sq_won': 'blue',
         'sq_not_won': 'black',
         'sq_mouseover': 'grey15',
         'button_bg': 'DodgerBlue1',
         }

# Need tk to match system's default white shade.
if platform_check.MY_OS == 'dar':  # macOS
    COLOR['tk_white'] = 'white'
elif platform_check.MY_OS == 'lin':  # Linux (Ubuntu)
    COLOR['tk_white'] = 'grey85'
else:  # platform is 'win'  # Windows (10)
    COLOR['tk_white'] = 'grey95'

FONT = {
    'sm_button': ('TkHeadingFont', 8),
    'who': ('TkHeadingFont', 7, 'italic bold'),
    'button': ('TkHeadingFont', 8, 'bold'),
    'scores': ('TkHeadingFont', 9),
    'status': ('TkHeadingFont', 9, 'italic bold'),
    'condensed': ('TkTooltipFont', 8),
    'mark': ('TkFixedFont', 52),
}

# Need to apply OS-specific font adjustments.
if platform_check.MY_OS == 'lin':
    FONT['status'] = ('TkHeadingFont', 10, 'italic bold')
elif platform_check.MY_OS == 'dar':
    FONT['sm_button'] = ('TkHeadingFont', 10)
    FONT['who'] = ('TkHeadingFont', 11, 'italic bold')
    FONT['button'] = ('TkHeadingFont', 11, 'bold')
    FONT['scores'] = ('TkHeadingFont', 13)
    FONT['status'] = ('TkHeadingFont', 13, 'italic bold')
    FONT['condensed'] = ('TkTooltipFont', 10)
    FONT['mark'] = ('TkFixedFont', 75)

# TIES (32) and WINS (1884) are all possible end-game board configurations,
#   in index order; 3 rows x 3 col indices: 012345678.
TIES = (
    'OOXXOOOXX', 'OOXXXOOOX', 'OOXXXOOXO', 'OOXXXOOXX', 'OXOOOXXOX', 'OXOOXOXOX',
    'OXOOXXXOO', 'OXOOXXXOX', 'OXOXOOXOX', 'OXOXOXXOX', 'OXOXXOOOX', 'OXOXXOXOX',
    'OXXXOOOOX', 'OXXXOOOXX', 'OXXXOOXOX', 'OXXXXOOOX', 'XOOOOXXXO', 'XOOOXXOXO',
    'XOOOXXXOO', 'XOOOXXXXO', 'XOXOOXOXO', 'XOXOOXXXO', 'XOXOXOOXO', 'XOXOXXOXO',
    'XOXXOOOXO', 'XOXXOOOXX', 'XOXXOXOXO', 'XOXXXOOXO', 'XXOOOXXOO', 'XXOOOXXOX',
    'XXOOOXXXO', 'XXOOXXXOO'
)

WINS = (
    'OOOOXXOXX', 'OOOOXXXOX', 'OOOOXXXXO', 'OOOOXXXXn', 'OOOOXXXnX', 'OOOOXXXnn',
    'OOOOXXnXX', 'OOOOXXnXn', 'OOOOXXnnX', 'OOOOXnXXn', 'OOOOXnXnX', 'OOOOXnnXX',
    'OOOOnXXXn', 'OOOOnXXnX', 'OOOOnXnXX', 'OOOXOXOXX', 'OOOXOXXOX', 'OOOXOXXXO',
    'OOOXOXXXn', 'OOOXOXXnX', 'OOOXOXXnn', 'OOOXOXnXX', 'OOOXOXnXn', 'OOOXOXnnX',
    'OOOXOnXXn', 'OOOXOnXnX', 'OOOXOnnXX', 'OOOXXOOXX', 'OOOXXOXOX', 'OOOXXOXXO',
    'OOOXXOXXn', 'OOOXXOXnX', 'OOOXXOXnn', 'OOOXXOnXX', 'OOOXXOnXn', 'OOOXXOnnX',
    'OOOXXnOXX', 'OOOXXnOXn', 'OOOXXnOnX', 'OOOXXnXOX', 'OOOXXnXOn', 'OOOXXnXXO',
    'OOOXXnXnO', 'OOOXXnXnn', 'OOOXXnnOX', 'OOOXXnnXO', 'OOOXXnnXn', 'OOOXXnnnX',
    'OOOXXnnnn', 'OOOXnOXXn', 'OOOXnOXnX', 'OOOXnOnXX', 'OOOXnXOXX', 'OOOXnXOXn',
    'OOOXnXOnX', 'OOOXnXXOX', 'OOOXnXXOn', 'OOOXnXXXO', 'OOOXnXXnO', 'OOOXnXXnn',
    'OOOXnXnOX', 'OOOXnXnXO', 'OOOXnXnXn', 'OOOXnXnnX', 'OOOXnXnnn', 'OOOXnnOXX',
    'OOOXnnXOX', 'OOOXnnXXO', 'OOOXnnXXn', 'OOOXnnXnX', 'OOOXnnXnn', 'OOOXnnnXX',
    'OOOXnnnXn', 'OOOXnnnnX', 'OOOnOXXXn', 'OOOnOXXnX', 'OOOnOXnXX', 'OOOnXOXXn',
    'OOOnXOXnX', 'OOOnXOnXX', 'OOOnXXOXX', 'OOOnXXOXn', 'OOOnXXOnX', 'OOOnXXXOX',
    'OOOnXXXOn', 'OOOnXXXXO', 'OOOnXXXnO', 'OOOnXXXnn', 'OOOnXXnOX', 'OOOnXXnXO',
    'OOOnXXnXn', 'OOOnXXnnX', 'OOOnXXnnn', 'OOOnXnOXX', 'OOOnXnXOX', 'OOOnXnXXO',
    'OOOnXnXXn', 'OOOnXnXnX', 'OOOnXnXnn', 'OOOnXnnXX', 'OOOnXnnXn', 'OOOnXnnnX',
    'OOOnnXOXX', 'OOOnnXXOX', 'OOOnnXXXO', 'OOOnnXXXn', 'OOOnnXXnX', 'OOOnnXXnn',
    'OOOnnXnXX', 'OOOnnXnXn', 'OOOnnXnnX', 'OOOnnnXXn', 'OOOnnnXnX', 'OOOnnnnXX',
    'OOXOOXXXO', 'OOXOOXXXX', 'OOXOOXXnX', 'OOXOOXnXX', 'OOXOOnXXX', 'OOXOXOOXX',
    'OOXOXOXXX', 'OOXOXOXXn', 'OOXOXOXnX', 'OOXOXXOXO', 'OOXOXXOXn', 'OOXOXXOnn',
    'OOXOXXXOX', 'OOXOXXXOn', 'OOXOXXXXO', 'OOXOXXXnO', 'OOXOXXXnn', 'OOXOXXnOX',
    'OOXOXXnnX', 'OOXOXnOXX', 'OOXOXnOXn', 'OOXOXnOnX', 'OOXOXnXOX', 'OOXOXnXXO',
    'OOXOXnXXn', 'OOXOXnXnX', 'OOXOXnXnn', 'OOXOnOXXX', 'OOXOnXOXn', 'OOXOnXXOX',
    'OOXOnXXnX', 'OOXOnXnXX', 'OOXOnXnnX', 'OOXOnnOXX', 'OOXOnnXXX', 'OOXXOOXOX',
    'OOXXOOXXO', 'OOXXOOXXX', 'OOXXOXOXO', 'OOXXOXOXX', 'OOXXOXOnX', 'OOXXOXXOO',
    'OOXXOXXOn', 'OOXXOXXnO', 'OOXXOXnOn', 'OOXXOXnXO', 'OOXXOXnnO', 'OOXXOXnnX',
    'OOXXOnXOX', 'OOXXOnXOn', 'OOXXOnXXO', 'OOXXOnXnO', 'OOXXOnnOX', 'OOXXOnnXO',
    'OOXXXOXOX', 'OOXXXOXOn', 'OOXXXOXXO', 'OOXXXOXnO', 'OOXXXOXnn', 'OOXXXXOOX',
    'OOXXXXOOn', 'OOXXXXOXO', 'OOXXXXOnO', 'OOXXXXOnn', 'OOXXXXXOO', 'OOXXXXnOO',
    'OOXXXXnOn', 'OOXXXXnnO', 'OOXXXnXOO', 'OOXXXnXOn', 'OOXXXnXnO', 'OOXXnXOOX',
    'OOXXnXOnX', 'OOXXnXnOX', 'OOXnOOXXX', 'OOXnOXOXX', 'OOXnOXXOn', 'OOXnOXXXO',
    'OOXnOXXnO', 'OOXnOXXnX', 'OOXnOXnXO', 'OOXnOXnXX', 'OOXnOXnnX', 'OOXnOnXOX',
    'OOXnOnXXO', 'OOXnOnXXX', 'OOXnXOXOX', 'OOXnXOXXO', 'OOXnXOXXn', 'OOXnXOXnX',
    'OOXnXOXnn', 'OOXnXXOOX', 'OOXnXXOnX', 'OOXnXXXOO', 'OOXnXXXOn', 'OOXnXXXnO',
    'OOXnXXnOX', 'OOXnXnXOX', 'OOXnXnXOn', 'OOXnXnXXO', 'OOXnXnXnO', 'OOXnXnXnn',
    'OOXnnOXXX', 'OOXnnXOXX', 'OOXnnXOnX', 'OOXnnXXOX', 'OOXnnXnOX', 'OOXnnXnnX',
    'OOnOOXXXX', 'OOnOXOXXX', 'OOnOXXOXX', 'OOnOXXOXn', 'OOnOXXOnX', 'OOnOXnOXX',
    'OOnOXnXXX', 'OOnOnXOXX', 'OOnOnXXXX', 'OOnOnnXXX', 'OOnXOOXXX', 'OOnXOXXOX',
    'OOnXOXXOn', 'OOnXOXXXO', 'OOnXOXXnO', 'OOnXOXnOX', 'OOnXOXnXO', 'OOnXOnXOX',
    'OOnXOnXXO', 'OOnXOnXXX', 'OOnXXXOOX', 'OOnXXXOXO', 'OOnXXXOXn', 'OOnXXXOnX',
    'OOnXXXOnn', 'OOnXXXXOO', 'OOnXXXXOn', 'OOnXXXXnO', 'OOnXXXnOX', 'OOnXXXnOn',
    'OOnXXXnXO', 'OOnXXXnnO', 'OOnXXXnnn', 'OOnXnOXXX', 'OOnnOXXOX', 'OOnnOXXXO',
    'OOnnOXXXX', 'OOnnOnXXX', 'OOnnXOXXX', 'OOnnnOXXX', 'OOnnnnXXX', 'OXOOOXOXX',
    'OXOOOXXXO', 'OXOOOXXXX', 'OXOOOnXXX', 'OXOOXOXXX', 'OXOOXOXXn', 'OXOOXOnXX',
    'OXOOXXOOX', 'OXOOXXOnX', 'OXOOXXOnn', 'OXOOXXXXO', 'OXOOXXnXO', 'OXOOXXnXn',
    'OXOOXnOnX', 'OXOOXnXXO', 'OXOOXnXXn', 'OXOOXnnXX', 'OXOOXnnXn', 'OXOOnOXXX',
    'OXOOnXOXX', 'OXOOnXOXn', 'OXOOnXOnX', 'OXOOnnOXX', 'OXOOnnXXX', 'OXOXOOOXX',
    'OXOXOOXXO', 'OXOXOOXXX', 'OXOXOXOOX', 'OXOXOXOXO', 'OXOXOXOXn', 'OXOXOXOnX',
    'OXOXOXOnn', 'OXOXOXXOO', 'OXOXOXXnO', 'OXOXOXnXO', 'OXOXOXnnO', 'OXOXOnOXX',
    'OXOXOnOXn', 'OXOXOnOnX', 'OXOXOnXXO', 'OXOXOnXnO', 'OXOXOnnXO', 'OXOXXOOXX',
    'OXOXXOOXn', 'OXOXXOXOO', 'OXOXXOXnO', 'OXOXXOnXn', 'OXOXXOnnO', 'OXOXXXOOX',
    'OXOXXXOOn', 'OXOXXXOXO', 'OXOXXXOnO', 'OXOXXXOnn', 'OXOXXXXOO', 'OXOXXXnOO',
    'OXOXXXnOn', 'OXOXXXnnO', 'OXOXXnOXO', 'OXOXXnOXn', 'OXOXXnnXO', 'OXOXnOXXO',
    'OXOXnOXnO', 'OXOXnOnXO', 'OXOnOOXXX', 'OXOnOXOXX', 'OXOnOXOXn', 'OXOnOXOnX',
    'OXOnOXXXO', 'OXOnOXXnO', 'OXOnOXnXO', 'OXOnOnOXX', 'OXOnOnXXO', 'OXOnOnXXX',
    'OXOnXOOXX', 'OXOnXOXXn', 'OXOnXOXnO', 'OXOnXOnXX', 'OXOnXOnXn', 'OXOnXXOXO',
    'OXOnXXOXn', 'OXOnXXnXO', 'OXOnXnOXX', 'OXOnXnOXn', 'OXOnXnXXO', 'OXOnXnnXO',
    'OXOnXnnXn', 'OXOnnOXXO', 'OXOnnOXXX', 'OXXOOOOXX', 'OXXOOOXOX', 'OXXOOOXXO',
    'OXXOOOXXn', 'OXXOOOXnX', 'OXXOOOXnn', 'OXXOOOnXX', 'OXXOOOnXn', 'OXXOOOnnX',
    'OXXOOXOXO', 'OXXOOXOXn', 'OXXOOXOnn', 'OXXOOXXOO', 'OXXOOXXOX', 'OXXOOXXnO',
    'OXXOOXnOX', 'OXXOOXnXO', 'OXXOOXnnO', 'OXXOOXnnX', 'OXXOOnOXX', 'OXXOOnOXn',
    'OXXOOnOnX', 'OXXOOnXXO', 'OXXOOnXnO', 'OXXOOnnXO', 'OXXOXOOOX', 'OXXOXOOnX',
    'OXXOXOOnn', 'OXXOXOXOX', 'OXXOXOXOn', 'OXXOXOXXO', 'OXXOXOXnO', 'OXXOXOXnn',
    'OXXOXOnXO', 'OXXOXOnXn', 'OXXOXXOOO', 'OXXOXXOOn', 'OXXOXXOnO', 'OXXOXXXOO',
    'OXXOXnOOX', 'OXXOXnOOn', 'OXXOXnOnO', 'OXXOXnOnn', 'OXXOXnXOO', 'OXXOXnXOn',
    'OXXOXnXnO', 'OXXOXnnXO', 'OXXOnOOXX', 'OXXOnOOXn', 'OXXOnOOnX', 'OXXOnXOOn',
    'OXXOnXOXO', 'OXXOnXOnO', 'OXXOnXOnn', 'OXXOnXnOX', 'OXXOnnOOX', 'OXXOnnOXO',
    'OXXOnnOXn', 'OXXOnnOnX', 'OXXOnnOnn', 'OXXXOOOXO', 'OXXXOOXOO', 'OXXXOOXnO',
    'OXXXOOnXO', 'OXXXOOnnO', 'OXXXOXOOO', 'OXXXOXOOX', 'OXXXOXOnO', 'OXXXOXnOO',
    'OXXXOnOXO', 'OXXXOnOnO', 'OXXXOnXOO', 'OXXXOnnOO', 'OXXXOnnnO', 'OXXXXOOOO',
    'OXXXXOOXO', 'OXXXXOXOO', 'OXXXXnOOO', 'OXXXnXOOO', 'OXXXnnOOO', 'OXXnOOXXO',
    'OXXnOOXnO', 'OXXnOOnXO', 'OXXnOXOOX', 'OXXnOXOXO', 'OXXnOXOnO', 'OXXnOXOnX',
    'OXXnOXXOO', 'OXXnOXnOO', 'OXXnOXnOX', 'OXXnOXnnO', 'OXXnOnOXO', 'OXXnOnXOO',
    'OXXnOnXnO', 'OXXnOnnXO', 'OXXnOnnnO', 'OXXnXOOXO', 'OXXnXOOXn', 'OXXnXOXOO',
    'OXXnXOXOn', 'OXXnXOXnO', 'OXXnXOnXO', 'OXXnXXOOO', 'OXXnXnOOO', 'OXXnXnOXO',
    'OXXnXnXOO', 'OXXnnXOOO', 'OXXnnXOOX', 'OXnOOOXXn', 'OXnOOOXnX', 'OXnOOOnXX',
    'OXnOOXOXX', 'OXnOOXOXn', 'OXnOOXOnX', 'OXnOOXXXO', 'OXnOOXXnO', 'OXnOOXnXO',
    'OXnOOnOXX', 'OXnOOnXXO', 'OXnOOnXXX', 'OXnOXOOnX', 'OXnOXOXXO', 'OXnOXOXXn',
    'OXnOXOnXX', 'OXnOXOnXn', 'OXnOXXOOX', 'OXnOXXOOn', 'OXnOXXOnO', 'OXnOXXOnn',
    'OXnOXXnXO', 'OXnOXnOOX', 'OXnOXnOnX', 'OXnOXnOnn', 'OXnOXnXXO', 'OXnOXnnXO',
    'OXnOXnnXn', 'OXnOnOOXX', 'OXnOnOXXX', 'OXnOnXOOX', 'OXnOnXOXO', 'OXnOnXOXn',
    'OXnOnXOnX', 'OXnOnXOnn', 'OXnOnnOXX', 'OXnOnnOXn', 'OXnOnnOnX', 'OXnXOOXXO',
    'OXnXOOXnO', 'OXnXOOnXO', 'OXnXOXOXO', 'OXnXOXOnO', 'OXnXOXXOO', 'OXnXOXnOO',
    'OXnXOXnnO', 'OXnXOnOXO', 'OXnXOnXOO', 'OXnXOnXnO', 'OXnXOnnXO', 'OXnXOnnnO',
    'OXnXXOOXO', 'OXnXXOOXn', 'OXnXXOnXO', 'OXnXXXOOn', 'OXnXXXOnO', 'OXnXXXnOO',
    'OXnXXnOOO', 'OXnXXnOXO', 'OXnXnXOOO', 'OXnnOOXXO', 'OXnnOOXXX', 'OXnnOXOXO',
    'OXnnOXXOO', 'OXnnOXXnO', 'OXnnOXnXO', 'OXnnOXnnO', 'OXnnOnXXO', 'OXnnOnXnO',
    'OXnnOnnXO', 'OXnnXOOXX', 'OXnnXOOXn', 'OXnnXOXXO', 'OXnnXOnXO', 'OXnnXOnXn',
    'OXnnXXOOO', 'OXnnXXOXO', 'OXnnXnOXO', 'OXnnXnOXn', 'OXnnXnnXO', 'OnOOOXXXX',
    'OnOOXOXXX', 'OnOOXXOXX', 'OnOOXXOXn', 'OnOOXXOnX', 'OnOOXnOXX', 'OnOOXnXXX',
    'OnOOnXOXX', 'OnOOnXXXX', 'OnOOnnXXX', 'OnOXOOXXX', 'OnOXOXOXX', 'OnOXOXOXn',
    'OnOXOXOnX', 'OnOXOXXXO', 'OnOXOXXnO', 'OnOXOXnXO', 'OnOXOnOXX', 'OnOXOnXXO',
    'OnOXOnXXX', 'OnOXXOXXO', 'OnOXXOXnO', 'OnOXXOnXO', 'OnOXXXOOX', 'OnOXXXOXO',
    'OnOXXXOXn', 'OnOXXXOnX', 'OnOXXXOnn', 'OnOXXXXOO', 'OnOXXXXOn', 'OnOXXXXnO',
    'OnOXXXnOX', 'OnOXXXnOn', 'OnOXXXnXO', 'OnOXXXnnO', 'OnOXXXnnn', 'OnOXnOXXO',
    'OnOXnOXXX', 'OnOnOXOXX', 'OnOnOXXXO', 'OnOnOXXXX', 'OnOnOnXXX', 'OnOnXOXXO',
    'OnOnXOXXX', 'OnOnnOXXX', 'OnOnnnXXX', 'OnXOOOXXn', 'OnXOOOXnX', 'OnXOOOnXX',
    'OnXOOXOXn', 'OnXOOXXOX', 'OnXOOXXXO', 'OnXOOXXnO', 'OnXOOXXnX', 'OnXOOXnXO',
    'OnXOOXnXX', 'OnXOOXnnX', 'OnXOOnOXX', 'OnXOOnXXO', 'OnXOOnXXX', 'OnXOXOOXX',
    'OnXOXOOXn', 'OnXOXOOnX', 'OnXOXOXOX', 'OnXOXOXXO', 'OnXOXOXXn', 'OnXOXOXnX',
    'OnXOXOXnn', 'OnXOXXOOn', 'OnXOXXOXO', 'OnXOXXOnO', 'OnXOXXOnn', 'OnXOXXXOO',
    'OnXOXXXOn', 'OnXOXXXnO', 'OnXOXXnOX', 'OnXOXnOOX', 'OnXOXnOXO', 'OnXOXnOXn',
    'OnXOXnOnX', 'OnXOXnOnn', 'OnXOXnXOX', 'OnXOXnXOn', 'OnXOXnXXO', 'OnXOXnXnO',
    'OnXOXnXnn', 'OnXOnOOXX', 'OnXOnOXXX', 'OnXOnXOXO', 'OnXOnXOXn', 'OnXOnXOnn',
    'OnXOnXXOX', 'OnXOnXnOX', 'OnXOnXnnX', 'OnXOnnOXX', 'OnXOnnOXn', 'OnXOnnOnX',
    'OnXXOOXXO', 'OnXXOOXnO', 'OnXXOOnXO', 'OnXXOXOOX', 'OnXXOXOXO', 'OnXXOXOnO',
    'OnXXOXOnX', 'OnXXOXXOO', 'OnXXOXnOO', 'OnXXOXnOX', 'OnXXOXnnO', 'OnXXOnOXO',
    'OnXXOnXOO', 'OnXXOnXnO', 'OnXXOnnXO', 'OnXXOnnnO', 'OnXXXOXOO', 'OnXXXOXOn',
    'OnXXXOXnO', 'OnXXXXOOn', 'OnXXXXOnO', 'OnXXXXnOO', 'OnXXXnOOO', 'OnXXXnXOO',
    'OnXXnXOOO', 'OnXXnXOOX', 'OnXnOOXXO', 'OnXnOOXXX', 'OnXnOXOXO', 'OnXnOXOXX',
    'OnXnOXOnX', 'OnXnOXXOO', 'OnXnOXXOX', 'OnXnOXXnO', 'OnXnOXnOX', 'OnXnOXnXO',
    'OnXnOXnnO', 'OnXnOXnnX', 'OnXnOnXXO', 'OnXnOnXnO', 'OnXnOnnXO', 'OnXnXOXOX',
    'OnXnXOXOn', 'OnXnXOXXO', 'OnXnXOXnO', 'OnXnXOXnn', 'OnXnXXOOO', 'OnXnXXOOX',
    'OnXnXXXOO', 'OnXnXnXOO', 'OnXnXnXOn', 'OnXnXnXnO', 'OnXnnXOOX', 'OnXnnXOnX',
    'OnXnnXnOX', 'OnnOOXOXX', 'OnnOOXXXO', 'OnnOOXXXX', 'OnnOOnXXX', 'OnnOXOOXX',
    'OnnOXOXXX', 'OnnOXXOOX', 'OnnOXXOXO', 'OnnOXXOXn', 'OnnOXXOnX', 'OnnOXXOnn',
    'OnnOXnOXX', 'OnnOXnOXn', 'OnnOXnOnX', 'OnnOnOXXX', 'OnnOnXOXX', 'OnnOnXOXn',
    'OnnOnXOnX', 'OnnOnnOXX', 'OnnOnnXXX', 'OnnXOOXXO', 'OnnXOOXXX', 'OnnXOXOXO',
    'OnnXOXXOO', 'OnnXOXXnO', 'OnnXOXnXO', 'OnnXOXnnO', 'OnnXOnXXO', 'OnnXOnXnO',
    'OnnXOnnXO', 'OnnXXXOOX', 'OnnXXXOOn', 'OnnXXXOXO', 'OnnXXXOnO', 'OnnXXXOnn',
    'OnnXXXXOO', 'OnnXXXnOO', 'OnnXXXnOn', 'OnnXXXnnO', 'OnnnOOXXX', 'OnnnOXXXO',
    'OnnnOXXnO', 'OnnnOXnXO', 'OnnnOnXXO', 'OnnnOnXXX', 'OnnnnOXXX', 'XOOOOXOXX',
    'XOOOOXXOX', 'XOOOOXXXX', 'XOOOOnXXX', 'XOOOXOXXO', 'XOOOXOXXX', 'XOOOXOXnX',
    'XOOOXOnXX', 'XOOOXXOXX', 'XOOOXXOnX', 'XOOOXXXOX', 'XOOOXXnOX', 'XOOOXXnnX',
    'XOOOXnOXX', 'XOOOXnXOX', 'XOOOXnXnX', 'XOOOXnnXX', 'XOOOXnnnX', 'XOOOnOXXX',
    'XOOOnnXXX', 'XOOXOOOXX', 'XOOXOOXXX', 'XOOXOOXXn', 'XOOXOOXnX', 'XOOXOXOOX',
    'XOOXOXOXO', 'XOOXOXOXn', 'XOOXOXOnX', 'XOOXOXOnn', 'XOOXOXXXO', 'XOOXOXXnO',
    'XOOXOXXnn', 'XOOXOXnOX', 'XOOXOXnOn', 'XOOXOnOXX', 'XOOXOnOXn', 'XOOXOnOnX',
    'XOOXOnXXO', 'XOOXOnXXn', 'XOOXOnXnX', 'XOOXOnXnn', 'XOOXOnnOX', 'XOOXXOOXO',
    'XOOXXOOXX', 'XOOXXOOnX', 'XOOXXOXOX', 'XOOXXOXOn', 'XOOXXOXnn', 'XOOXXOnOX',
    'XOOXXOnXO', 'XOOXXOnnO', 'XOOXXOnnX', 'XOOXXXOOX', 'XOOXXXOOn', 'XOOXXXOXO',
    'XOOXXXOnO', 'XOOXXXOnn', 'XOOXXXXOO', 'XOOXXXnOO', 'XOOXXXnOn', 'XOOXXXnnO',
    'XOOXXnOOX', 'XOOXXnOnX', 'XOOXXnXOO', 'XOOXXnXOn', 'XOOXXnXnO', 'XOOXXnnOX',
    'XOOXnOXOX', 'XOOXnOXXn', 'XOOXnOXnX', 'XOOXnOXnn', 'XOOXnOnXO', 'XOOXnXXOO',
    'XOOXnXXOn', 'XOOXnXXnO', 'XOOXnnXOX', 'XOOXnnXOn', 'XOOXnnXXO', 'XOOXnnXnO',
    'XOOXnnXnn', 'XOOnOOXXX', 'XOOnOXOXX', 'XOOnOXOXn', 'XOOnOXOnX', 'XOOnOXXOX',
    'XOOnOXXOn', 'XOOnOXnOX', 'XOOnOnOXX', 'XOOnOnXOX', 'XOOnOnXXX', 'XOOnXOOXX',
    'XOOnXOXOX', 'XOOnXOXXO', 'XOOnXOXnO', 'XOOnXOXnX', 'XOOnXOnXO', 'XOOnXOnXX',
    'XOOnXOnnX', 'XOOnXXOOX', 'XOOnXXOnX', 'XOOnXXnOX', 'XOOnXnOXX', 'XOOnXnOnX',
    'XOOnXnXOX', 'XOOnXnnOX', 'XOOnXnnnX', 'XOOnnOXXO', 'XOOnnOXXX', 'XOXOOOOXX',
    'XOXOOOXOX', 'XOXOOOXXO', 'XOXOOOXXn', 'XOXOOOXnX', 'XOXOOOXnn', 'XOXOOOnXX',
    'XOXOOOnXn', 'XOXOOOnnX', 'XOXOOXOXX', 'XOXOOXOnX', 'XOXOOXXOO', 'XOXOOXXOn',
    'XOXOOXnOn', 'XOXOOXnnX', 'XOXOOnXOX', 'XOXOOnXOn', 'XOXOOnnOX', 'XOXOXOOXX',
    'XOXOXOOnX', 'XOXOXOXOX', 'XOXOXOXOn', 'XOXOXOXXO', 'XOXOXOXnO', 'XOXOXOXnn',
    'XOXOXOnOX', 'XOXOXOnnX', 'XOXOXXOOO', 'XOXOXXOOX', 'XOXOXXXOO', 'XOXOXnOOX',
    'XOXOXnOnX', 'XOXOXnXOO', 'XOXOXnXOn', 'XOXOXnXnO', 'XOXOXnnOX', 'XOXOnXOOX',
    'XOXOnXOnX', 'XOXOnXnOX', 'XOXXOOOOX', 'XOXXOOXXO', 'XOXXOOXnO', 'XOXXOOXnn',
    'XOXXOOnOX', 'XOXXOOnOn', 'XOXXOXOOO', 'XOXXOXOOn', 'XOXXOXnOO', 'XOXXOnOOX',
    'XOXXOnOOn', 'XOXXOnXnO', 'XOXXOnnOO', 'XOXXOnnOn', 'XOXXXOOOO', 'XOXXXOOOX',
    'XOXXXOXOO', 'XOXXXnOOO', 'XOXXnOXOO', 'XOXXnOXOn', 'XOXXnOXnO', 'XOXXnXOOO',
    'XOXXnnOOO', 'XOXXnnXOO', 'XOXnOOXOX', 'XOXnOOXOn', 'XOXnOOnOX', 'XOXnOXOOn',
    'XOXnOXOnX', 'XOXnOXXOO', 'XOXnOXnOO', 'XOXnOXnOn', 'XOXnOnOOX', 'XOXnOnXOO',
    'XOXnOnXOn', 'XOXnOnnOX', 'XOXnOnnOn', 'XOXnXOOOX', 'XOXnXOOnX', 'XOXnXOXOO',
    'XOXnXOXOn', 'XOXnXOXnO', 'XOXnXOnOX', 'XOXnXXOOO', 'XOXnXnOOO', 'XOXnXnOOX',
    'XOXnXnXOO', 'XOXnnXOOO', 'XOXnnXOOX', 'XOnOOOXXn', 'XOnOOOXnX', 'XOnOOOnXX',
    'XOnOOXXOX', 'XOnOOXXOn', 'XOnOOXnOX', 'XOnOOnXOX', 'XOnOOnXXX', 'XOnOXOOXX',
    'XOnOXOXOX', 'XOnOXOXnX', 'XOnOXOnXX', 'XOnOXOnnX', 'XOnOXXOOX', 'XOnOXXOnX',
    'XOnOXXnOX', 'XOnOXnOXX', 'XOnOXnOnX', 'XOnOXnXOX', 'XOnOXnnOX', 'XOnOXnnnX',
    'XOnOnOXXX', 'XOnXOOXXO', 'XOnXOOXXn', 'XOnXOOXnX', 'XOnXOOXnn', 'XOnXOOnOX',
    'XOnXOXOOX', 'XOnXOXOOn', 'XOnXOXXnO', 'XOnXOXnOO', 'XOnXOXnOn', 'XOnXOnOOX',
    'XOnXOnXXO', 'XOnXOnXnO', 'XOnXOnXnn', 'XOnXOnnOX', 'XOnXOnnOn', 'XOnXXOOOX',
    'XOnXXOOnX', 'XOnXXOXOO', 'XOnXXOXOn', 'XOnXXOXnO', 'XOnXXOnOX', 'XOnXXXOOn',
    'XOnXXXOnO', 'XOnXXXnOO', 'XOnXXnOOO', 'XOnXXnOOX', 'XOnXXnXOO', 'XOnXnOXOX',
    'XOnXnOXOn', 'XOnXnOXXO', 'XOnXnOXnO', 'XOnXnOXnn', 'XOnXnXOOO', 'XOnXnXXOO',
    'XOnXnnXOO', 'XOnXnnXOn', 'XOnXnnXnO', 'XOnnOOXOX', 'XOnnOOXXX', 'XOnnOXOOX',
    'XOnnOXXOO', 'XOnnOXXOn', 'XOnnOXnOX', 'XOnnOXnOn', 'XOnnOnXOX', 'XOnnOnXOn',
    'XOnnOnnOX', 'XOnnXOOXX', 'XOnnXOOnX', 'XOnnXOXOX', 'XOnnXOnOX', 'XOnnXOnnX',
    'XOnnXXOOO', 'XOnnXXOOX', 'XOnnXnOOX', 'XOnnXnOnX', 'XOnnXnnOX', 'XXOOOOOXX',
    'XXOOOOXOX', 'XXOOOOXXO', 'XXOOOOXXn', 'XXOOOOXnX', 'XXOOOOXnn', 'XXOOOOnXX',
    'XXOOOOnXn', 'XXOOOOnnX', 'XXOOOXOOX', 'XXOOOXOXO', 'XXOOOXOXn', 'XXOOOXOnX',
    'XXOOOXOnn', 'XXOOOnOXX', 'XXOOOnOXn', 'XXOOOnOnX', 'XXOOXOOXX', 'XXOOXOOXn',
    'XXOOXOOnX', 'XXOOXOXOO', 'XXOOXOXOX', 'XXOOXOXnO', 'XXOOXOnOX', 'XXOOXOnXn',
    'XXOOXOnnO', 'XXOOXOnnX', 'XXOOXXOOO', 'XXOOXXOOX', 'XXOOXXOXO', 'XXOOXnOOX',
    'XXOOXnOXO', 'XXOOXnOXn', 'XXOOXnOnX', 'XXOOXnnOX', 'XXOOXnnXO', 'XXOOnOXXO',
    'XXOOnOXnO', 'XXOOnOnXO', 'XXOXOOOOX', 'XXOXOOOXO', 'XXOXOOOXn', 'XXOXOOOnX',
    'XXOXOOOnn', 'XXOXOOXOX', 'XXOXOOXOn', 'XXOXOOXnn', 'XXOXOOnXO', 'XXOXOOnnO',
    'XXOXOXOOO', 'XXOXOXOOn', 'XXOXOXOnO', 'XXOXOXXOO', 'XXOXOnOOX', 'XXOXOnOOn',
    'XXOXOnOXO', 'XXOXOnOnO', 'XXOXOnOnn', 'XXOXOnXOO', 'XXOXOnXOn', 'XXOXOnXnO',
    'XXOXXOOOO', 'XXOXXOOOX', 'XXOXXOOnO', 'XXOXXOnOO', 'XXOXXnOOO', 'XXOXnOOXO',
    'XXOXnOOnO', 'XXOXnOXOn', 'XXOXnOnOO', 'XXOXnOnnO', 'XXOXnXOOO', 'XXOXnnOOO',
    'XXOXnnXOO', 'XXOnOOOXX', 'XXOnOOOXn', 'XXOnOOOnX', 'XXOnOOXXO', 'XXOnOOXnO',
    'XXOnOOnXO', 'XXOnOXOOX', 'XXOnOXOOn', 'XXOnOXOXO', 'XXOnOXOnO', 'XXOnOXOnn',
    'XXOnOnOOX', 'XXOnOnOXO', 'XXOnOnOXn', 'XXOnOnOnX', 'XXOnOnOnn', 'XXOnXOOOX',
    'XXOnXOOXn', 'XXOnXOOnO', 'XXOnXOOnX', 'XXOnXOXOO', 'XXOnXOnOO', 'XXOnXOnOX',
    'XXOnXOnnO', 'XXOnXXOOO', 'XXOnXnOOO', 'XXOnXnOOX', 'XXOnXnOXO', 'XXOnnOOXO',
    'XXOnnOXOO', 'XXOnnOXnO', 'XXOnnOnXO', 'XXOnnOnnO', 'XXOnnXOOO', 'XXXOOXOOX',
    'XXXOOXOOn', 'XXXOOXOXO', 'XXXOOXOnO', 'XXXOOXOnn', 'XXXOOXXOO', 'XXXOOXnOO',
    'XXXOOXnOn', 'XXXOOXnnO', 'XXXOOnOOX', 'XXXOOnOXO', 'XXXOOnOXn', 'XXXOOnOnX',
    'XXXOOnOnn', 'XXXOOnXOO', 'XXXOOnXOn', 'XXXOOnXnO', 'XXXOOnnOX', 'XXXOOnnOn',
    'XXXOOnnXO', 'XXXOOnnnO', 'XXXOOnnnn', 'XXXOXOOOX', 'XXXOXOOOn', 'XXXOXOOXO',
    'XXXOXOOnO', 'XXXOXOOnn', 'XXXOXOXOO', 'XXXOXOnOO', 'XXXOXOnOn', 'XXXOXOnnO',
    'XXXOXnOOn', 'XXXOXnOnO', 'XXXOXnnOO', 'XXXOnOOOX', 'XXXOnOOXO', 'XXXOnOOXn',
    'XXXOnOOnX', 'XXXOnOOnn', 'XXXOnOXOO', 'XXXOnOXOn', 'XXXOnOXnO', 'XXXOnOnOX',
    'XXXOnOnOn', 'XXXOnOnXO', 'XXXOnOnnO', 'XXXOnOnnn', 'XXXOnXOOn', 'XXXOnXOnO',
    'XXXOnXnOO', 'XXXOnnOOX', 'XXXOnnOOn', 'XXXOnnOXO', 'XXXOnnOnO', 'XXXOnnOnn',
    'XXXOnnXOO', 'XXXOnnnOO', 'XXXOnnnOn', 'XXXOnnnnO', 'XXXXOOOOX', 'XXXXOOOOn',
    'XXXXOOOXO', 'XXXXOOOnO', 'XXXXOOOnn', 'XXXXOOXOO', 'XXXXOOnOO', 'XXXXOOnOn',
    'XXXXOOnnO', 'XXXXOnOOn', 'XXXXOnOnO', 'XXXXOnnOO', 'XXXXnOOOn', 'XXXXnOOnO',
    'XXXXnOnOO', 'XXXnOOOOX', 'XXXnOOOXO', 'XXXnOOOXn', 'XXXnOOOnX', 'XXXnOOOnn',
    'XXXnOOXOO', 'XXXnOOXOn', 'XXXnOOXnO', 'XXXnOOnOX', 'XXXnOOnOn', 'XXXnOOnXO',
    'XXXnOOnnO', 'XXXnOOnnn', 'XXXnOXOOn', 'XXXnOXOnO', 'XXXnOXnOO', 'XXXnOnOOX',
    'XXXnOnOOn', 'XXXnOnOXO', 'XXXnOnOnO', 'XXXnOnOnn', 'XXXnOnXOO', 'XXXnOnnOO',
    'XXXnOnnOn', 'XXXnOnnnO', 'XXXnXOOOn', 'XXXnXOOnO', 'XXXnXOnOO', 'XXXnnOOOX',
    'XXXnnOOOn', 'XXXnnOOXO', 'XXXnnOOnO', 'XXXnnOOnn', 'XXXnnOXOO', 'XXXnnOnOO',
    'XXXnnOnOn', 'XXXnnOnnO', 'XXXnnnOOn', 'XXXnnnOnO', 'XXXnnnnOO', 'XXnOOOOXX',
    'XXnOOOOXn', 'XXnOOOOnX', 'XXnOOOXOX', 'XXnOOOXOn', 'XXnOOOXXO', 'XXnOOOXnO',
    'XXnOOOXnn', 'XXnOOOnOX', 'XXnOOOnXO', 'XXnOOOnXn', 'XXnOOOnnX', 'XXnOOOnnn',
    'XXnOXOOOX', 'XXnOXOOXO', 'XXnOXOOXn', 'XXnOXOOnX', 'XXnOXOnOX', 'XXnOXOnXO',
    'XXnOXXOOO', 'XXnOXnOOO', 'XXnOXnOOX', 'XXnOXnOXO', 'XXnOnXOOO', 'XXnXOOXOO',
    'XXnXOOXOn', 'XXnXOOXnO', 'XXnXOXOOO', 'XXnXOnOOO', 'XXnXOnXOO', 'XXnXXOOOO',
    'XXnXnOOOO', 'XXnXnOXOO', 'XXnXnnOOO', 'XXnnOXOOO', 'XXnnXOOOO', 'XXnnXOOOX',
    'XXnnXOOXO', 'XXnnXnOOO', 'XXnnnXOOO', 'XXnnnnOOO', 'XnOOOOXXn', 'XnOOOOXnX',
    'XnOOOOnXX', 'XnOOOXOXX', 'XnOOOXOXn', 'XnOOOXOnX', 'XnOOOnOXX', 'XnOOOnXXX',
    'XnOOXOOXX', 'XnOOXOXOX', 'XnOOXOXXO', 'XnOOXOXnO', 'XnOOXOXnX', 'XnOOXOnXO',
    'XnOOXOnXX', 'XnOOXOnnX', 'XnOOXXOOX', 'XnOOXXOnX', 'XnOOXXnOX', 'XnOOXnOXX',
    'XnOOXnOnX', 'XnOOXnXOX', 'XnOOXnnOX', 'XnOOXnnnX', 'XnOOnOXXO', 'XnOOnOXXX',
    'XnOXOOOXX', 'XnOXOOOXn', 'XnOXOOOnX', 'XnOXOOXOX', 'XnOXOOXXn', 'XnOXOOXnX',
    'XnOXOOXnn', 'XnOXOOnXO', 'XnOXOXOOX', 'XnOXOXOOn', 'XnOXOXOXO', 'XnOXOXOnO',
    'XnOXOXOnn', 'XnOXOXXOO', 'XnOXOXXOn', 'XnOXOXXnO', 'XnOXOnOOX', 'XnOXOnOXO',
    'XnOXOnOXn', 'XnOXOnOnX', 'XnOXOnOnn', 'XnOXOnXOX', 'XnOXOnXOn', 'XnOXOnXXO',
    'XnOXOnXnO', 'XnOXOnXnn', 'XnOXXOOOX', 'XnOXXOOXO', 'XnOXXOOnO', 'XnOXXOOnX',
    'XnOXXOXOn', 'XnOXXOnOO', 'XnOXXOnOX', 'XnOXXOnnO', 'XnOXXXOOn', 'XnOXXXOnO',
    'XnOXXXnOO', 'XnOXXnOOO', 'XnOXXnOOX', 'XnOXXnXOO', 'XnOXnOOXO', 'XnOXnOXOX',
    'XnOXnOXOn', 'XnOXnOXnn', 'XnOXnOnXO', 'XnOXnOnnO', 'XnOXnXOOO', 'XnOXnXXOO',
    'XnOXnnXOO', 'XnOXnnXOn', 'XnOXnnXnO', 'XnOnOOOXX', 'XnOnOOXXO', 'XnOnOOXXX',
    'XnOnOXOOX', 'XnOnOXOXO', 'XnOnOXOXn', 'XnOnOXOnX', 'XnOnOXOnn', 'XnOnOnOXX',
    'XnOnOnOXn', 'XnOnOnOnX', 'XnOnXOOXO', 'XnOnXOOXX', 'XnOnXOOnX', 'XnOnXOXOO',
    'XnOnXOXOX', 'XnOnXOXnO', 'XnOnXOnOX', 'XnOnXOnXO', 'XnOnXOnnO', 'XnOnXOnnX',
    'XnOnXXOOO', 'XnOnXXOOX', 'XnOnXnOOX', 'XnOnXnOnX', 'XnOnXnnOX', 'XnOnnOXXO',
    'XnOnnOXnO', 'XnOnnOnXO', 'XnXOOOOXX', 'XnXOOOOXn', 'XnXOOOOnX', 'XnXOOOXOX',
    'XnXOOOXOn', 'XnXOOOXXO', 'XnXOOOXnO', 'XnXOOOXnn', 'XnXOOOnOX', 'XnXOOOnXO',
    'XnXOOOnXn', 'XnXOOOnnX', 'XnXOOOnnn', 'XnXOOXOOX', 'XnXOOXOnX', 'XnXOOXnOX',
    'XnXOXOOOX', 'XnXOXOOnX', 'XnXOXOXOO', 'XnXOXOXOn', 'XnXOXOXnO', 'XnXOXOnOX',
    'XnXOXXOOO', 'XnXOXnOOO', 'XnXOXnOOX', 'XnXOXnXOO', 'XnXOnXOOO', 'XnXOnXOOX',
    'XnXXOOXOO', 'XnXXOOXOn', 'XnXXOOXnO', 'XnXXOXOOO', 'XnXXOnOOO', 'XnXXOnXOO',
    'XnXXXOOOO', 'XnXXnOOOO', 'XnXXnOXOO', 'XnXXnnOOO', 'XnXnOXOOO', 'XnXnOXOOX',
    'XnXnXOOOO', 'XnXnXOOOX', 'XnXnXOXOO', 'XnXnXnOOO', 'XnXnnXOOO', 'XnXnnnOOO',
    'XnnOOOOXX', 'XnnOOOXOX', 'XnnOOOXXO', 'XnnOOOXXn', 'XnnOOOXnX', 'XnnOOOXnn',
    'XnnOOOnXX', 'XnnOOOnXn', 'XnnOOOnnX', 'XnnOXOOXX', 'XnnOXOOnX', 'XnnOXOXOX',
    'XnnOXOnOX', 'XnnOXOnnX', 'XnnOXXOOO', 'XnnOXXOOX', 'XnnOXnOOX', 'XnnOXnOnX',
    'XnnOXnnOX', 'XnnXOOXOX', 'XnnXOOXOn', 'XnnXOOXXO', 'XnnXOOXnO', 'XnnXOOXnn',
    'XnnXOXOOO', 'XnnXOXXOO', 'XnnXOnXOO', 'XnnXOnXOn', 'XnnXOnXnO', 'XnnXXOOOO',
    'XnnXXOOOX', 'XnnXXOXOO', 'XnnXXnOOO', 'XnnXnOXOO', 'XnnXnOXOn', 'XnnXnOXnO',
    'XnnXnXOOO', 'XnnXnnOOO', 'XnnXnnXOO', 'XnnnXOOOX', 'XnnnXOOnX', 'XnnnXOnOX',
    'XnnnXXOOO', 'XnnnXnOOO', 'XnnnXnOOX', 'XnnnnXOOO', 'nOOOOXXXX', 'nOOOXOXXX',
    'nOOOXnXXX', 'nOOOnXXXX', 'nOOOnnXXX', 'nOOXOOXXX', 'nOOXOXOXX', 'nOOXOXOXn',
    'nOOXOXOnX', 'nOOXOXXOX', 'nOOXOXXOn', 'nOOXOXnOX', 'nOOXOnOXX', 'nOOXOnXOX',
    'nOOXOnXXX', 'nOOXXOXXO', 'nOOXXOXnO', 'nOOXXOnXO', 'nOOXXXOOX', 'nOOXXXOXO',
    'nOOXXXOXn', 'nOOXXXOnX', 'nOOXXXOnn', 'nOOXXXXOO', 'nOOXXXXOn', 'nOOXXXXnO',
    'nOOXXXnOX', 'nOOXXXnOn', 'nOOXXXnXO', 'nOOXXXnnO', 'nOOXXXnnn', 'nOOXnOXXO',
    'nOOXnOXXX', 'nOOnOXOXX', 'nOOnOXXOX', 'nOOnOXXXX', 'nOOnOnXXX', 'nOOnXOXXO',
    'nOOnXOXXX', 'nOOnnOXXX', 'nOOnnnXXX', 'nOXOOOXXn', 'nOXOOOXnX', 'nOXOOOnXX',
    'nOXOOXOXX', 'nOXOOXXOn', 'nOXOOXXnX', 'nOXOOXnXX', 'nOXOOXnnX', 'nOXOOnXOX',
    'nOXOOnXXX', 'nOXOXOXOX', 'nOXOXOXXO', 'nOXOXOXXn', 'nOXOXOXnX', 'nOXOXOXnn',
    'nOXOXXOOX', 'nOXOXXOnX', 'nOXOXXXOO', 'nOXOXXXOn', 'nOXOXXXnO', 'nOXOXXnOX',
    'nOXOXnXOX', 'nOXOXnXOn', 'nOXOXnXXO', 'nOXOXnXnO', 'nOXOXnXnn', 'nOXOnOXXX',
    'nOXOnXOXX', 'nOXOnXOnX', 'nOXOnXXOX', 'nOXOnXnOX', 'nOXOnXnnX', 'nOXXOOXOX',
    'nOXXOOXOn', 'nOXXOOnOX', 'nOXXOXOOn', 'nOXXOXOnX', 'nOXXOXXOO', 'nOXXOXnOO',
    'nOXXOXnOn', 'nOXXOnOOX', 'nOXXOnXOO', 'nOXXOnXOn', 'nOXXOnnOX', 'nOXXOnnOn',
    'nOXXXOXOO', 'nOXXXOXOn', 'nOXXXOXnO', 'nOXXXXOOn', 'nOXXXXOnO', 'nOXXXXnOO',
    'nOXXXnOOO', 'nOXXXnXOO', 'nOXXnXOOO', 'nOXXnXOOX', 'nOXnOOXOX', 'nOXnOOXXX',
    'nOXnOXOXX', 'nOXnOXOnX', 'nOXnOXXOO', 'nOXnOXXOn', 'nOXnOXnOn', 'nOXnOXnnX',
    'nOXnOnXOX', 'nOXnOnXOn', 'nOXnOnnOX', 'nOXnXOXOX', 'nOXnXOXOn', 'nOXnXOXXO',
    'nOXnXOXnO', 'nOXnXOXnn', 'nOXnXXOOO', 'nOXnXXOOX', 'nOXnXXXOO', 'nOXnXnXOO',
    'nOXnXnXOn', 'nOXnXnXnO', 'nOXnnXOOX', 'nOXnnXOnX', 'nOXnnXnOX', 'nOnOOXXOX',
    'nOnOOXXXX', 'nOnOOnXXX', 'nOnOXOXXX', 'nOnOnOXXX', 'nOnOnnXXX', 'nOnXOOXOX',
    'nOnXOOXXX', 'nOnXOXOOX', 'nOnXOXXOO', 'nOnXOXXOn', 'nOnXOXnOX', 'nOnXOXnOn',
    'nOnXOnXOX', 'nOnXOnXOn', 'nOnXOnnOX', 'nOnXXXOOX', 'nOnXXXOOn', 'nOnXXXOXO',
    'nOnXXXOnO', 'nOnXXXOnn', 'nOnXXXXOO', 'nOnXXXnOO', 'nOnXXXnOn', 'nOnXXXnnO',
    'nOnnOOXXX', 'nOnnOXXOX', 'nOnnOXXOn', 'nOnnOXnOX', 'nOnnOnXOX', 'nOnnOnXXX',
    'nOnnnOXXX', 'nXOOOOXXn', 'nXOOOOXnX', 'nXOOOOnXX', 'nXOOOXOXX', 'nXOOOXOXn',
    'nXOOOXOnX', 'nXOOOnOXX', 'nXOOOnXXX', 'nXOOXOOXX', 'nXOOXOXXn', 'nXOOXOXnO',
    'nXOOXOnXX', 'nXOOXOnXn', 'nXOOXXOXO', 'nXOOXXOXn', 'nXOOXXnXO', 'nXOOXnOXX',
    'nXOOXnOXn', 'nXOOXnXXO', 'nXOOXnnXO', 'nXOOXnnXn', 'nXOOnOXXO', 'nXOOnOXXX',
    'nXOXOOOXX', 'nXOXOOOXn', 'nXOXOOOnX', 'nXOXOOXXO', 'nXOXOOXnO', 'nXOXOOnXO',
    'nXOXOXOOX', 'nXOXOXOOn', 'nXOXOXOXO', 'nXOXOXOnO', 'nXOXOXOnn', 'nXOXOnOOX',
    'nXOXOnOXO', 'nXOXOnOXn', 'nXOXOnOnX', 'nXOXOnOnn', 'nXOXXOOXn', 'nXOXXOOnO',
    'nXOXXOXOO', 'nXOXXOnOO', 'nXOXXOnnO', 'nXOXXXOOn', 'nXOXXXOnO', 'nXOXXXnOO',
    'nXOXXnOOO', 'nXOXXnOXO', 'nXOXnOOXO', 'nXOXnOXOO', 'nXOXnOXnO', 'nXOXnOnXO',
    'nXOXnOnnO', 'nXOXnXOOO', 'nXOnOOOXX', 'nXOnOOXXO', 'nXOnOOXXX', 'nXOnOXOOX',
    'nXOnOXOXO', 'nXOnOXOXn', 'nXOnOXOnX', 'nXOnOXOnn', 'nXOnOnOXX', 'nXOnOnOXn',
    'nXOnOnOnX', 'nXOnXOOXX', 'nXOnXOOXn', 'nXOnXOXOO', 'nXOnXOXnO', 'nXOnXOnXn',
    'nXOnXOnnO', 'nXOnXXOOO', 'nXOnXXOXO', 'nXOnXnOXO', 'nXOnXnOXn', 'nXOnXnnXO',
    'nXOnnOXXO', 'nXOnnOXnO', 'nXOnnOnXO', 'nXXOOOOXX', 'nXXOOOOXn', 'nXXOOOOnX',
    'nXXOOOXOX', 'nXXOOOXOn', 'nXXOOOXXO', 'nXXOOOXnO', 'nXXOOOXnn', 'nXXOOOnOX',
    'nXXOOOnXO', 'nXXOOOnXn', 'nXXOOOnnX', 'nXXOOOnnn', 'nXXOOXOOX', 'nXXOOXOnX',
    'nXXOOXnOX', 'nXXOXOOXO', 'nXXOXOOXn', 'nXXOXOXOO', 'nXXOXOXOn', 'nXXOXOXnO',
    'nXXOXOnXO', 'nXXOXXOOO', 'nXXOXnOOO', 'nXXOXnOXO', 'nXXOXnXOO', 'nXXOnXOOO',
    'nXXOnXOOX', 'nXXXOXOOO', 'nXXXOnOOO', 'nXXXXOOOO', 'nXXXnOOOO', 'nXXXnnOOO',
    'nXXnOXOOO', 'nXXnOXOOX', 'nXXnXOOOO', 'nXXnXOOXO', 'nXXnXOXOO', 'nXXnXnOOO',
    'nXXnnXOOO', 'nXXnnnOOO', 'nXnOOOOXX', 'nXnOOOXOX', 'nXnOOOXXO', 'nXnOOOXXn',
    'nXnOOOXnX', 'nXnOOOXnn', 'nXnOOOnXX', 'nXnOOOnXn', 'nXnOOOnnX', 'nXnOXOOXX',
    'nXnOXOOXn', 'nXnOXOXXO', 'nXnOXOnXO', 'nXnOXOnXn', 'nXnOXXOOO', 'nXnOXXOXO',
    'nXnOXnOXO', 'nXnOXnOXn', 'nXnOXnnXO', 'nXnXOXOOO', 'nXnXXOOOO', 'nXnXXOOXO',
    'nXnXXnOOO', 'nXnXnXOOO', 'nXnXnnOOO', 'nXnnXOOXO', 'nXnnXOOXn', 'nXnnXOnXO',
    'nXnnXXOOO', 'nXnnXnOOO', 'nXnnXnOXO', 'nXnnnXOOO', 'nnOOOXOXX', 'nnOOOXXXX',
    'nnOOOnXXX', 'nnOOXOXXO', 'nnOOXOXXX', 'nnOOnOXXX', 'nnOOnnXXX', 'nnOXOOOXX',
    'nnOXOOXXO', 'nnOXOOXXX', 'nnOXOXOOX', 'nnOXOXOXO', 'nnOXOXOXn', 'nnOXOXOnX',
    'nnOXOXOnn', 'nnOXOnOXX', 'nnOXOnOXn', 'nnOXOnOnX', 'nnOXXOOXO', 'nnOXXOXOO',
    'nnOXXOXnO', 'nnOXXOnXO', 'nnOXXOnnO', 'nnOXXXOOX', 'nnOXXXOOn', 'nnOXXXOXO',
    'nnOXXXOnO', 'nnOXXXOnn', 'nnOXXXXOO', 'nnOXXXnOO', 'nnOXXXnOn', 'nnOXXXnnO',
    'nnOXnOXXO', 'nnOXnOXnO', 'nnOXnOnXO', 'nnOnOOXXX', 'nnOnOXOXX', 'nnOnOXOXn',
    'nnOnOXOnX', 'nnOnOnOXX', 'nnOnOnXXX', 'nnOnXOXXO', 'nnOnXOXnO', 'nnOnXOnXO',
    'nnOnnOXXO', 'nnOnnOXXX', 'nnXOOOOXX', 'nnXOOOXOX', 'nnXOOOXXO', 'nnXOOOXXn',
    'nnXOOOXnX', 'nnXOOOXnn', 'nnXOOOnXX', 'nnXOOOnXn', 'nnXOOOnnX', 'nnXOOXOXX',
    'nnXOOXOnX', 'nnXOOXXOX', 'nnXOOXnOX', 'nnXOOXnnX', 'nnXOXOXOX', 'nnXOXOXOn',
    'nnXOXOXXO', 'nnXOXOXnO', 'nnXOXOXnn', 'nnXOXXOOO', 'nnXOXXOOX', 'nnXOXXXOO',
    'nnXOXnXOO', 'nnXOXnXOn', 'nnXOXnXnO', 'nnXOnXOOX', 'nnXOnXOnX', 'nnXOnXnOX',
    'nnXXOXOOO', 'nnXXOXOOX', 'nnXXXOOOO', 'nnXXXOXOO', 'nnXXXnOOO', 'nnXXnXOOO',
    'nnXXnnOOO', 'nnXnOXOOX', 'nnXnOXOnX', 'nnXnOXnOX', 'nnXnXOXOO', 'nnXnXOXOn',
    'nnXnXOXnO', 'nnXnXXOOO', 'nnXnXnOOO', 'nnXnXnXOO', 'nnXnnXOOO', 'nnXnnXOOX',
    'nnnOOOXXn', 'nnnOOOXnX', 'nnnOOOnXX', 'nnnOOnXXX', 'nnnOnOXXX', 'nnnXXXOOn',
    'nnnXXXOnO', 'nnnXXXnOO', 'nnnXXnOOO', 'nnnXnXOOO', 'nnnnOOXXX', 'nnnnXXOOO'
)

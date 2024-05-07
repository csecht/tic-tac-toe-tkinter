#!/usr/bin/env python3

"""
ttt.py is a tkinter GUI offering various play modes of the Tic Tac Toe
game. The objective is to win a game by getting three of your player's
marks (either X or O) in a row on a 3x3 game board.
Play mode options:
  Player v Player,
  Player v PC (with PC preference options),
  Autoplay, about 120 games of the PC playing itself in either random,
    strategic, or center-first mode options, with an option for either
    always starting with same player or alternating start turns.

Requires tkinter (tk/tcl) and Python3.6+.
Developed in Python 3.8-3.9 with tkinter 8.6.

Inspired by Riya Tendulkar code:
https://levelup.gitconnected.com/how-to-code-tic-tac-toe-in-python-using-tkinter-e7f9ce510bfb
https://gist.github.com/riya1620/72c2b668ef29da061c44d97a82318572
"""
# Copyright: (c) 2022 Craig S. Echt, under MIT License

# Standard library imports:
import random
from typing import Callable  # Used only in auto_repeat()

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except (ImportError, ModuleNotFoundError) as error:
    print(f'This program requires tkinter, which is included with \n'
          'Python 3.7+ distributions.\n'
          'Install the most recent version or re-install Python and include Tk/Tcl.\n'
          '\nLinux users may need this: $ sudo apt-get install python3-tk\n'
          f'See also: https://tkdocs.com/tutorial/install.html \n{error}')

# Local program imports:
from ttt_utils import vcheck, grid_this, utils
from ttt_utils.constants import (
    AUTO_FAST,
    AUTO_SLOW,
    COLOR,
    CORNERS,
    FONT,
    MARKS1,
    MARKS2,
    META_POSITIONS,
    MY_OS,
    ORTHO_SIDES,
    P1_MARK,
    P2_MARK,
    PARA_CORNERS,
    PLAY_AFTER,
    PLAYER1,
    PLAYER2,
    SIDES,
    WINNING_COMBOS,
)


class TicTacToeGUI(tk.Tk):
    """
    Display the tkinter GUI playing board and its control buttons.
    Provide multiple modes of play action, with scoring.
    Methods: auto_command, auto_flash_game, auto_setup, auto_start,
    auto_stop, play_rudiments, autoplay_center,
    autoplay_random, autoplay_tactics, autospeed_control,
    autostart_who, check_winner, color_pc_mark, configure_widgets,
    display_status, highlight_result, grid_widgets, human_turn,
    mode_control, new_game, play_defense, pc_turn,
    play_random, reset_game_and_score, setup_game_board, turn_number,
    unbind_game_board, window_geometry, ready_player_one
    """
    # Using __slots__ for all Class attributes gives slight reduction of
    #   memory usage and maybe improved performance.
    __slots__ = (
        'after_id', 'auto_marks',
        'auto_start_stop_btn', 'auto_center_mode', 'auto_random_mode',
        'auto_tactics_mode', 'auto_turns_header', 'auto_turns_lbl',
        'auto_turns_remaining', 'autospeed_fast', 'autospeed_slow',
        'autospeed_lbl', 'autospeed_selection',
        'board_labels', 'choose_pc_pref', 'pc_pref',
        'curr_pmode', 'curr_automode', 'mode_clicked',
        'p1_points', 'p1_score', 'p2_points', 'p2_score',
        'player1_header', 'player1_score_lbl',
        'player2_header', 'player2_score_lbl',
        'prev_game_num', 'prev_game_num_header', 'prev_game_num_lbl',
        'pvp_mode', 'pvpc_mode', 'quit_button',
        'status_calls', 'statuswin_geometry',
        'score_header', 'separator', 'ties_header', 'ties_lbl',
        'ties_num', 'titlebar_offset', 'who_autostarts_btn', 'whose_turn',
        'whose_turn_lbl', 'winner_found',
    )

    def __init__(self):
        super().__init__()

        # Game stats widgets and variables.
        self.p1_points = 0
        self.p2_points = 0
        self.p1_score = tk.IntVar()
        self.p2_score = tk.IntVar()
        self.prev_game_num_header = tk.Label()
        self.prev_game_num = tk.IntVar()
        self.prev_game_num_lbl = tk.Label()

        # Player's turn widgets.
        self.whose_turn = tk.StringVar()
        self.whose_turn_lbl = tk.Label()
        self.auto_turns_header = tk.Label()
        self.auto_turns_lbl = tk.Label()
        self.auto_turns_remaining = tk.IntVar()

        # Players' scores widgets.
        self.score_header = tk.Label()
        self.player1_header = tk.Label()
        self.player2_header = tk.Label()
        self.player1_score_lbl = tk.Label()
        self.player2_score_lbl = tk.Label()
        self.ties_header = tk.Label()
        self.ties_num = tk.IntVar()
        self.ties_lbl = tk.Label()

        # Play action widgets.
        self.board_labels = [tk.Label() for _ in range(9)]
        self.mode_clicked = tk.StringVar()
        self.pvp_mode = tk.Radiobutton()
        self.pvpc_mode = tk.Radiobutton()
        self.pc_pref = tk.StringVar()
        self.choose_pc_pref = ttk.Combobox()

        self.auto_random_mode = tk.Radiobutton()
        self.auto_tactics_mode = tk.Radiobutton()
        self.auto_center_mode = tk.Radiobutton()
        self.auto_start_stop_btn = ttk.Button()
        self.who_autostarts_btn = ttk.Button()
        self.autospeed_selection = tk.StringVar()
        self.autospeed_lbl = tk.Label()
        self.autospeed_fast = tk.Radiobutton()
        self.autospeed_slow = tk.Radiobutton()

        # Game Status window variables.
        self.statuswin_geometry = ''  # Current Game Status window position.
        self.status_calls = 0  # Used as flag to set titlebar_offset.
        self.titlebar_offset = 0  # Used to properly position Game Status window.

        # Additional widgets and variables.
        self.separator = ttk.Separator()
        self.after_id = None  # A handler for after() and after_cancel() calls.
        self.auto_marks = ''  # Used to dole out autoplay marks in proper register.
        self.curr_automode = ''  # Used to display whose_turn.
        self.curr_pmode = ''  # Used to evaluate mode state.
        self.winner_found = False  # Used for game flow control.
        self.quit_button = ttk.Button()

        self.grid_widgets()
        self.configure_widgets()
        self.setup_game_board()

    def grid_widgets(self) -> None:
        """Position mainloop (app, self) window widgets."""

        # Position play action Labels in 3 x 3 grid. Note that while
        #   nothing is gridded in row index 1, the top row uses rowspan=2
        #   to center widgets vertically; hence, board_labels begin on
        #   row index 2.
        # Grid parameters of board_labels determine the height and width
        #   of the app window.
        _row = 2
        _col = 0

        # Set platform-specific padding between board squares (board_labels).
        if MY_OS == 'win':  # Windows
            pad = 8
            ipadx = 10
            ipady = 6
        elif MY_OS == 'lin':  # Linux
            pad = 0
            ipadx = 10
            ipady = 6
        else:  # macOS
            pad = 6
            ipadx = 0
            ipady = 0

        for lbl in self.board_labels:
            lbl.grid(row=_row, column=_col,
                     padx=pad, pady=pad,
                     ipadx=ipadx, ipady=ipady)
            _col += 1
            # Grid 3 labels in 3 columns, then move to next row and repeat.
            if _col > 2:
                _row += 1
                _col = 0

        # Developer: see all gridded objects against contrasting background.
        # self.config(bg='purple')

        # All other OS-specific widget grid calls are in the grid_this module.
        # In these calls, 'self' refers to the mainloop, 'app', this Class.
        if MY_OS == 'win':
            grid_this.windows(self)
        elif MY_OS == 'lin':
            grid_this.linux(self)
        else:
            grid_this.mac(self)

    def configure_widgets(self) -> None:
        """Initial configurations of mainloop window widgets."""
        ttk.Style().theme_use('alt')
        utils.keybindings(self, 'quit_keys')
        utils.keybindings(self, 'bind_board')

        self.prev_game_num.set(0)
        self.ties_num.set(0)

        # ttk.Buttons are used b/c tk.Buttons cannot be configured in macOS.
        style = ttk.Style()
        style.map('My.TButton',
                  foreground=[('pressed', COLOR['disabled_fg']),
                              ('active', COLOR['mark_fg']),
                              ('disabled', COLOR['disabled_fg']),
                              ],
                  background=[('pressed', COLOR['tk_white']),
                              ('active', COLOR['button_bg']),
                              ]
                  )
        style.configure('My.TButton', font=FONT['button'])

        # Player's turn widgets.
        self.prev_game_num_header.config(text='Games played',
                                         font=FONT['condensed'])
        self.prev_game_num_lbl.config(textvariable=self.prev_game_num,
                                      font=FONT['condensed'])

        whose_w = 13 if MY_OS == 'dar' else 16  # is Linux or Windows
        self.whose_turn_lbl.config(textvariable=self.whose_turn,
                                   font=FONT['who'],
                                   height=4,
                                   width=whose_w)

        self.ready_player_one()  # Starting prompt for Player1 to begin play.
        self.auto_turns_header.config(text='Turns to go',
                                      font=FONT['condensed'],
                                      fg=COLOR['tk_white'])  # match default bg.
        self.auto_turns_lbl.config(textvariable=self.auto_turns_remaining,
                                   font=FONT['condensed'],
                                   fg=COLOR['tk_white'])  # match default bg.

        score_params = dict(
            font=FONT['scores'],
            fg=COLOR['score_fg'])

        # Players' scores widgets:
        # Squiggle symbol, '︴', from https://coolsymbol.com/line-symbols.html
        self.score_header.config(text='Score ︴', **score_params)
        self.player1_header.config(text=f'{PLAYER1}:', **score_params)
        self.player2_header.config(text=f'{PLAYER2}:', **score_params)
        self.player1_score_lbl.config(textvariable=self.p1_score, **score_params)
        self.player2_score_lbl.config(textvariable=self.p2_score, **score_params)
        self.ties_header.config(text='Ties:', **score_params)
        self.ties_lbl.config(textvariable=self.ties_num, **score_params)

        # Play mode control widgets:
        self.pvp_mode.config(text='Player v Player',
                             font=FONT['condensed'],
                             variable=self.mode_clicked,
                             value='pvp',
                             command=self.mode_control)
        self.pvp_mode.select()  # Set mode at startup.

        self.pvpc_mode.config(text='Player v PC',
                              font=FONT['condensed'],
                              variable=self.mode_clicked,
                              value='pvpc',
                              command=self.mode_control)

        # choose_pc_pref is enabled as readonly when pvpc_mode is selected.
        #   Set drop-down list font size to match displayed font size.
        self.choose_pc_pref.config(textvariable=self.pc_pref,
                                   font=FONT['condensed'],
                                   width=15,
                                   values=('PC plays random',
                                           'PC plays center',
                                           'PC plays tactics'),
                                   state=tk.DISABLED)
        self.option_add("*TCombobox*Font", FONT['condensed'])
        self.choose_pc_pref.bind('<<ComboboxSelected>>',
                                 lambda _: self.reset_game_and_score())
        #  Set 'PC plays random', 1st in tuple, as the startup default.
        self.choose_pc_pref.current(0)

        self.separator.configure(orient='horizontal')

        self.auto_random_mode.config(text='Autoplay random',
                                     font=FONT['condensed'],
                                     variable=self.mode_clicked,
                                     value='Autoplay random',
                                     command=self.mode_control)
        self.auto_center_mode.config(text='Autoplay center',
                                     font=FONT['condensed'],
                                     variable=self.mode_clicked,
                                     value='Autoplay center',
                                     command=self.mode_control)
        self.auto_tactics_mode.config(text='Autoplay tactics',
                                      font=FONT['condensed'],
                                      variable=self.mode_clicked,
                                      value='Autoplay tactics',
                                      command=self.mode_control)
        self.autospeed_lbl.config(text='Auto-speed',
                                  font=FONT['condensed'])
        self.autospeed_fast.config(text='Fast',
                                   font=FONT['condensed'],
                                   variable=self.autospeed_selection,
                                   value='fast',
                                   command=self.autospeed_control)
        self.autospeed_slow.config(text='Slow',
                                   font=FONT['condensed'],
                                   variable=self.autospeed_selection,
                                   value='slow',
                                   command=self.autospeed_control)
        # Set startup auto-speed to 'slow'.
        self.autospeed_slow.select()

        # Configure ttk Buttons.
        self.auto_start_stop_btn.config(text='Start Autoplay',
                                        style='My.TButton',
                                        width=0,
                                        state=tk.DISABLED,
                                        command=self.auto_command)
        self.who_autostarts_btn.configure(text='Player 1 starts',
                                          style='My.TButton',
                                          width=14,
                                          state=tk.DISABLED,
                                          command=self.autostart_who)
        self.quit_button.config(text='Quit',
                                style='My.TButton',
                                width=4,
                                command=lambda: utils.quit_game(mainloop=self))

    def setup_game_board(self) -> None:
        """
        Configure and activate play action for the game board squares.

        :return: None
        """

        # Functions to change square backgrounds with mouseover & leave.
        def on_enter(label: tk) -> None:
            if label['bg'] == COLOR['sq_not_won'] and label['text'] == ' ':
                label['bg'] = COLOR['sq_mouseover']
            else:  # The square has already been played.
                label['bg'] = COLOR['sq_not_won']

        def on_leave(label: tk):
            if label['bg'] == COLOR['sq_mouseover']:
                label['bg'] = COLOR['sq_not_won']
            elif label['bg'] == COLOR['sq_not_won']:
                label['bg'] = COLOR['sq_not_won']

        # Reset game board squares to starting configurations.
        if MY_OS == 'dar':
            bd_w = 6
            hilite_w = 0
        else:  # is Linux or Windows.
            bd_w = 2  # default
            hilite_w = 5

        for i, lbl in enumerate(self.board_labels):
            lbl.config(text=' ',
                       width=2,  # number of characters
                       bg=COLOR['sq_not_won'],
                       fg=COLOR['mark_fg'],
                       font=FONT['mark'],
                       borderwidth=bd_w,
                       highlightthickness=hilite_w,
                       )

            if self.mode_clicked.get() in 'pvp, pvpc':
                lbl.bind('<Button-1>',
                         lambda event, lbl_idx=i:
                         self.human_turn(self.board_labels[lbl_idx])
                         )
                lbl.bind('<Enter>', lambda event, l=lbl: on_enter(l))
                lbl.bind('<Leave>', lambda event, l=lbl: on_leave(l))

    def unbind_game_board(self) -> None:
        """
        Prevent user action on game board squares.

        :return: None
        """
        for lbl in self.board_labels:
            lbl.unbind('<Button-1>')
            lbl.unbind('<Enter>')
            lbl.unbind('<Leave>')
        utils.keybindings(self, 'unbind_board')

    def disable(self, *group: str) -> None:
        """
        Groups of related statements to disable widget activity.

        :param group: The group(s) to disable. Use any or all:
                'player_modes', 'auto_modes', 'auto_controls'.
        :return: None
        """

        if 'player_modes' in group:
            self.pvp_mode.config(state=tk.DISABLED)
            self.pvpc_mode.config(state=tk.DISABLED)

        if 'auto_modes' in group:
            self.auto_random_mode.config(state=tk.DISABLED)
            self.auto_center_mode.config(state=tk.DISABLED)
            self.auto_tactics_mode.config(state=tk.DISABLED)

        if 'auto_controls' in group:
            self.auto_start_stop_btn.config(state=tk.DISABLED)
            self.who_autostarts_btn.configure(state=tk.DISABLED)
            self.autospeed_fast.config(state=tk.DISABLED)
            self.autospeed_slow.config(state=tk.DISABLED)

    def mode_control(self) -> None:
        """
        Block any mode change if in the middle of a game or in autoplay.

        Disable and enable Radiobuttons as each mode requires.
        Cancel/ignore an errant or mistimed play mode selection.
        Is callback from the play mode Radiobuttons.

        :return: None
        """
        mode_clicked = self.mode_clicked.get()

        # If a game is in progress, ignore any mode selections & post msg.
        if self.turn_number() > 0 and not self.winner_found:
            if mode_clicked in 'pvp, pvpc':
                self.disable('auto_modes', 'auto_controls')

                if self.curr_pmode == 'pvp':
                    self.pvp_mode.select()
                    self.pvpc_mode.config(state=tk.DISABLED)
                    self.pvpc_mode.deselect()
                elif self.curr_pmode == 'pvpc':
                    self.pvpc_mode.select()
                    self.pvp_mode.config(state=tk.DISABLED)
                    # Only allow changing pc prefs on Human (P1) turn;
                    #  this forces completion of a two-turn game cycle.
                    if self.prev_game_num.get() % 2 == 0:
                        self.choose_pc_pref.config(state='readonly')
                    self.pvp_mode.deselect()

                messagebox.showinfo(title='Mode is unavailable now',
                                    detail='Finish the current game,\n'
                                           'then change mode.')
        else:  # No game in progress.
            if mode_clicked == 'pvpc':
                self.choose_pc_pref.config(state='readonly')
                self.player2_header.config(text='PC:')
                # Need immediate replacement of header text.
                self.update_idletasks()
            else:
                self.choose_pc_pref.config(state=tk.DISABLED)
                self.player2_header.config(text=f'{PLAYER2}:')

            if mode_clicked in 'pvp, pvpc':
                self.disable('auto_controls')
                self.ready_player_one()
                utils.keybindings(self, 'bind_board')
            else:  # one of the auto modes was clicked.
                self.auto_start_stop_btn.config(state=tk.NORMAL)
                self.who_autostarts_btn.configure(state=tk.NORMAL)
                self.autospeed_fast.config(state=tk.NORMAL)
                self.autospeed_slow.config(state=tk.NORMAL)
                self.whose_turn.set(mode_clicked)
                self.curr_automode = mode_clicked
                self.whose_turn_lbl.config(bg=COLOR['tk_white'])

            self.reset_game_and_score()

    def ready_player_one(self) -> None:
        """
        Display when it is Human's (Player 1) turn after PC has played.
        Shout out to Steven Spielberg.

        :return: None
        """
        if self.mode_clicked.get() == 'pvpc' and self.turn_number() == 1:
            self.whose_turn.set(f'PC played {P2_MARK}\n'
                                f'Your turn {PLAYER1}')
        else:
            self.whose_turn.set(f'{PLAYER1} plays {P1_MARK}')

        self.whose_turn_lbl.config(bg=COLOR['status_bg'])

    def human_turn(self, played_lbl: tk) -> None:
        """
        Check whether *played_lbl* selected by player was already played.
        If not, assign player's mark to the text value of the selected
        label.
        Players' marks (X or O) alternate who has first the turn in
        consecutive games.
        Played squares are evaluated for a win after the 5th turn.

        :param played_lbl: The tk.Label object (the board_label square)
                           that was clicked.
        :return: None
        """

        def h_plays(mark: str, next_turn_msg: str) -> None:
            played_lbl['text'] = mark
            self.whose_turn.set(next_turn_msg)
            self.whose_turn_lbl.config(bg=COLOR['tk_white'])
            if mark == P2_MARK:
                played_lbl.config(fg=COLOR['tk_white'])

        # At start, Previous game # = 0, then increments after a win/tie.
        #  At start of a new game, turn # = 0.
        #  On even PvPC games, pc will have already played 1st turn.

        if played_lbl['text'] == ' ':
            self.disable('auto_modes', 'auto_controls')

            if self.mode_clicked.get() == 'pvp':
                self.curr_pmode = 'pvp'
                if self.prev_game_num.get() % 2 == self.turn_number() % 2:
                    h_plays(P1_MARK, f'{PLAYER2} plays {P2_MARK}')
                else:
                    h_plays(P2_MARK, f'{PLAYER1} plays {P1_MARK}')

                if self.turn_number() >= 5:
                    self.check_winner(played_lbl.cget('text'))

            else:  # The PvPC mode was clicked.
                self.curr_pmode = 'pvpc'
                if self.prev_game_num.get() % 2 == self.turn_number() % 2:
                    h_plays(P1_MARK, f'PC plays {P2_MARK}')

                self.update_idletasks()

                if self.turn_number() >= 5:
                    self.check_winner(P1_MARK)

                if self.turn_number() < 9 and not self.winner_found:
                    self.pc_turn()

            # Play is now underway so disable the Player v... mode that
            #  is not in play.
            if self.curr_pmode == 'pvp':
                self.pvpc_mode.config(state=tk.DISABLED)
            else:
                self.pvp_mode.config(state=tk.DISABLED)

        else:  # The played_lbl has a player's mark as its text.
            curr_player = PLAYER1 if PLAYER1 in self.whose_turn.get() else PLAYER2
            curr_mark = P1_MARK if PLAYER1 in self.whose_turn.get() else P2_MARK
            self.whose_turn.set(f'That square is\ntaken {curr_player}.\n'
                                f'Play {curr_mark} elsewhere.')

    def color_pc_mark(self, _id: int) -> None:
        """
        In PvPC mode, display alternate fg color for PC's mark text.
        Default color (COLOR['mark_fg']) for human (Player 1) is set in
        setup_game_board(), so change that to a white fg.

        :param _id: The board_labels list index of the played square.
        :return: None
        """

        self.board_labels[_id].config(fg=COLOR['tk_white'])

    def pc_turn(self) -> None:
        """
        Conditions for PC to play as Player2 (P2_MARK).
        Precedence of PC play: selected pref option > play for a win >
        block P1 win > play to corner, if preferred > play random.
        Called from human_turn() and new_game().
        Color PC mark as 'tk_white', which is the system's 'white'.

        :return: None
        """
        # Inspiration for basic play-action algorithm:
        # https://www.simplifiedpython.net/python-tic-tac-toe-using-artificial-intelligence/

        turn_number = self.turn_number()

        # Delay play for a better feel, but not when PC starts a game b/c
        #   that just delays closing the Game Status toplevel for a new game.
        if turn_number > 0:
            self.after(PLAY_AFTER)
            self.choose_pc_pref.config(state=tk.DISABLED)

        # Need to re-order winner list so Human doesn't detect a pattern
        #   of where PC will play.
        #   CORNERS list is shuffled in play_corners().
        random.shuffle(WINNING_COMBOS)

        """Turn number will advance following PC play from any of the
        play_xxx() methods used here in succession. If no play is made,
        turn_number will not advance, so the next play_xxx() method will
        be called."""

        # Preference: all PC moves are random.
        if self.choose_pc_pref.get() == 'PC plays random':
            self.play_random(turn_number, P2_MARK)

        # Preference: play the center when it is available.
        elif self.choose_pc_pref.get() == 'PC plays center':
            if self.board_labels[4]['text'] == ' ':
                self.board_labels[4]['text'] = P2_MARK
                self.color_pc_mark(4)

        # Now prefer to play for win, then for block.
        if turn_number == self.turn_number():
            self.play_rudiments(P2_MARK, pvpc=True)

        # Tactical preference: play a set of rules to minimize losses.
        if self.choose_pc_pref.get() == 'PC plays tactics':
            if turn_number == self.turn_number():
                self.play_defense(turn_number, P2_MARK, pvpc=True)

            # Fill in available corners to play for advantage.
            if turn_number == self.turn_number():
                self.play_corners(turn_number, P2_MARK, pvpc=True)

        # No preferred plays are available, so play random.
        if turn_number == self.turn_number():
            self.play_random(turn_number, P2_MARK)
            print('PC played randomly (nothing to block or win), '
                  f'Game {self.prev_game_num.get() + 1}:Turn {turn_number + 1}')

        if self.turn_number() >= 5:
            self.check_winner(P2_MARK)

        if not self.winner_found:
            self.ready_player_one()

        self.update_idletasks()

    def play_rudiments(self, mark: str, pvpc=False) -> None:
        """
        The rules engine for basic play to win or block.

        :param mark: The played mark string character.
        :param pvpc: Use when called from a P v PC mode (default, False).
        :returns: None
        """

        # Randomize the order of the WINNING_COMBOS list so Human
        #  can't detect a pattern of PC play.
        random.shuffle(WINNING_COMBOS)
        opponent = P2_MARK if mark == P1_MARK else P1_MARK

        # Note that running two loops is necessary to prioritize
        #  winning over blocking because need to first evaluate ALL
        #  possible winning moves before trying to block.
        # Use the count method to check if there are two marks in the
        #  positions and the index method to find an empty position.

        # First, play to win; check positions of current player's marks.
        #  If two player's marks are aligned, fill the empty third position.
        for combo in WINNING_COMBOS:
            _x, _y, _z = combo
            positions = [self.board_labels[pos]['text'] for pos in combo]
            empty_index = positions.index(' ') if ' ' in positions else None

            if positions.count(mark) == 2 and empty_index is not None:
                self.board_labels[combo[empty_index]]['text'] = mark
                if pvpc:
                    self.color_pc_mark(combo[empty_index])
                return

        # No win available, so play to block; check positions of opponent's marks.
        #  If two opponent's marks are aligned, play the empty third position.
        for combo in WINNING_COMBOS:
            _x, _y, _z = combo
            positions = [self.board_labels[pos]['text'] for pos in combo]
            empty_index = positions.index(' ') if ' ' in positions else None

            if positions.count(opponent) == 2 and empty_index is not None:
                self.board_labels[combo[empty_index]]['text'] = mark
                if pvpc:
                    self.color_pc_mark(combo[empty_index])
                break

    def play_defense(self, turn_number: int, mark: str, pvpc=False) -> None:
        """
        A rules-based set of defensive responses to minimize PC losses.
        Strategy in decreasing priority: defend center, sides, corners.

        :param turn_number: Current turn count from turn_number().
        :param mark: The played mark character, as string.
        :param pvpc: Use when called from a P v PC mode (default, False).

        :return: None
        """

        # Get opponent's mark and list indices of its played squares.
        oppo_mark = P2_MARK if mark == P1_MARK else P1_MARK
        oppo_list = [i for i in range(9) if self.board_labels[i]['text'] == oppo_mark]

        # Always defend center, if available, in response to opponent's 1st turn.
        if turn_number == 1:
            if self.board_labels[4]['text'] == ' ':
                self.board_labels[4]['text'] = mark
                if pvpc:
                    self.color_pc_mark(4)
                    print('PC grabbed the center, '
                          f'Game {self.prev_game_num.get() + 1}:Turn {turn_number + 1}')
        elif turn_number > 1:
            # When opponent plays a side square, play the open center to
            #  reduce possibility of a loss.
            if (self.board_labels[4]['text'] == ' ' and
                    oppo_mark in (self.board_labels[i]['text'] for i in SIDES)):
                self.board_labels[4]['text'] = mark
                if pvpc:
                    self.color_pc_mark(4)
                    print('PC played center defense, '
                          f'Game {self.prev_game_num.get() + 1}:Turn {turn_number + 1}')
                    return

            # When opponent is on two adjacent side squares, defend with play
            #   to the shared (nearest) corner.
            for key, val in ORTHO_SIDES.items():
                if self.board_labels[key]['text'] == ' ' and oppo_list == val:
                    self.board_labels[key]['text'] = mark
                    if pvpc:
                        self.color_pc_mark(key)
                        print('PC played corner for orthogonal sides defense, '
                              f'Game {self.prev_game_num.get() + 1}:Turn {turn_number + 1}')
                    return

            # When opponent has played a corner and a non-adjacent side, defend with
            #   play to opponent's shared (nearest) corner.
            for key, val in META_POSITIONS.items():
                if self.board_labels[key]['text'] == ' ' and oppo_list == val:
                    self.board_labels[key]['text'] = mark
                    if pvpc:
                        self.color_pc_mark(key)
                        print('PC played corner for meta-positional defense, '
                              f'Game {self.prev_game_num.get() + 1}:Turn {turn_number + 1}')
                    return

            # When opponent has played to opposite corners, defend with play to
            #   a random side.
            side2play = random.choice(SIDES)
            if oppo_list in PARA_CORNERS:
                self.board_labels[side2play]['text'] = mark
                if pvpc:
                    self.color_pc_mark(side2play)
                    print('PC played a side for para-corners defense,'
                          f' Game {self.prev_game_num.get() + 1}:Turn {turn_number + 1}')

    def play_corners(self, turn_number: int, mark: str, pvpc=False) -> None:
        """
        Fill in available corners to increase probability of a win.
        Used for 'tactics' play modes.

        :param turn_number: Current turn count from turn_number().
        :param mark: The played mark character, as string.
        :param pvpc: True when called from a P vs PC mode (default, False).

        :return: None
        """

        available_corners = [i for i in CORNERS if self.board_labels[i]['text'] == ' ']
        if available_corners and turn_number == self.turn_number():
            i = random.choice(available_corners)
            self.board_labels[i]['text'] = mark
            if pvpc:
                self.color_pc_mark(i)
                print(f'PC played corner tactics, Game {self.prev_game_num.get() + 1}:Turn {turn_number + 1}')

    def play_random(self, turn_number: int, mark: str) -> None:
        """ Play a random position in board_labels.

        :param turn_number: Current turn count from turn_number().
        :param mark: The player's mark string to play.

        :return: None
        """
        available_positions = [i for i in range(9) if self.board_labels[i]['text'] == ' ']
        if available_positions and turn_number == self.turn_number():
            random_idx = random.choice(available_positions)
            self.board_labels[random_idx]['text'] = mark
            if self.mode_clicked.get() in 'pvp, pvpc':
                self.color_pc_mark(random_idx)
    def turn_number(self) -> int:
        """
        Keep count of turns taken during a game.
        Count number of board_labels squares with text other than a space.

        :return: The number of turns played, as integer.
        """
        return len([i for i in self.board_labels if ' ' not in i['text']])

    def check_winner(self, mark: str) -> None:
        """Check played board_labels for a win or tie.

        :param mark: The played mark character to check for a win.
        :return: None
        """

        mode = self.mode_clicked.get()

        def award_points(winning_mark: str) -> None:
            """
            This uses the fact that Python treats True as 1 and False as
            0. So, if winning_mark is equal to P1_MARK,
            winning_mark == P1_MARK will be True and 1 will be added to
            p1_points. Otherwise, it will be False and 0 will be added.
            Similarly, if winning_mark is not equal to P1_MARK,
            winning_mark != P1_MARK will be True and 1 will be added to
            p2_points. Otherwise, it will be False and 0 will be added.
            (Thank you Copilot for the explanation.)
            :param winning_mark: Current player's mark
            :return: None
            """
            self.p1_points += winning_mark == P1_MARK
            self.p2_points += winning_mark != P1_MARK

        # Loop breaks when the first winning combo is found.
        for combo in WINNING_COMBOS:
            lbl_texts = [self.board_labels[i]['text'] for i in combo]

            if all(text == mark for text in lbl_texts):
                self.winner_found = True
                self.prev_game_num.set(self.prev_game_num.get() + 1)
                game = self.prev_game_num.get()
                turn = self.turn_number()

                award_points(mark)
                if 'Autoplay' in mode:
                    self.auto_flash_game(combo, mark)
                elif mode == 'pvpc':
                    self.highlight_result('win', combo)
                    display_message = 'PC WINS!' if mark == P2_MARK else 'You WIN!'
                    self.display_status(display_message)
                    if self.pc_pref.get() in ['PC plays tactics', 'PC plays center']:
                        winner = 'PC' if mark == P2_MARK else 'Human'
                        print(
                            f'{winner} won "{self.pc_pref.get()} mode", Game {game}:Turn {turn}.')
                else:
                    self.highlight_result('win', combo)
                    self.display_status(f'{mark} WINS!')
                break

        if self.turn_number() == 9 and not self.winner_found:  # Is a tie.
            self.winner_found = True
            self.prev_game_num.set(self.prev_game_num.get() + 1)

            # Record to file all tied board_labels lists.
            # tielist = f'{[i["text"] for i in self.board_labels]}\n'
            # with open('ties', 'a') as file:
            #     file.write(tielist)

            self.p1_points += 0.5
            self.p2_points += 0.5

            self.ties_num.set(self.ties_num.get() + 1)

            if 'Autoplay' in mode:
                self.auto_flash_game((4, 4, 4), 'TIE')
            else:  # Mode selection is pvp or pvpc.
                self.highlight_result('tie')
                self.display_status('IT IS A TIE!')
                self.whose_turn.set('Game pending...')
                self.whose_turn_lbl.config(bg=COLOR['tk_white'])

                # Print is not needed here for 'PC plays random'.
                if self.pc_pref.get() in 'PC plays tactics, PC plays center':
                    print('-Tie-')

    def highlight_result(self, status: str, combo=None) -> None:
        """
        Change color of board squares depending on game result.

        Derived from Bryan Oakley's answer for
        how-to-make-a-button-flash-using-after-in-tkinter
        https://stackoverflow.com/a/57298778
        :param status: End game result, either 'win' or 'tie'.
        :param combo: Tuple of the three winning board_labels indices,
                      or None (default) for a tie.
        :return: None
        """
        if status == 'win':
            _x, _y, _z = combo

            self.after(10, lambda: self.board_labels[_x].config(bg=COLOR['sq_won']))
            self.after(175, lambda: self.board_labels[_y].config(bg=COLOR['sq_won']))
            self.after(345, lambda: self.board_labels[_z].config(bg=COLOR['sq_won']))

        else:  # status is 'tie'
            for lbl in self.board_labels:
                lbl.config(bg=COLOR['sq_won'])
                self.update_idletasks()

    def window_geometry(self, toplevel: tk) -> None:
        """
        Set xy pixel coordinates of a window in relation to main tk window.

        If toplevel is moved during a play session, then draw it at its
        new xy position for subsequent calls; position is determined by
        functions in display_status().
        Calculate the height of the system's window title bar to use as
        a y-offset for the *toplevel* xy geometry.

        :param toplevel: The tkinter toplevel object to position.
        :return: None
        """

        if self.statuswin_geometry:
            toplevel.geometry(self.statuswin_geometry)
        else:
            toplevel.geometry(f'+{self.winfo_x()}+{self.winfo_y()}')

        # Need to position the geometry of the Report window by applying
        #   a y offset for the height of the system's window title bar.
        #   This is needed because tkinter widget geometry does not
        #   include the system's title bar.
        # Title bar height is determined only once from the default
        #   placement of the Report window at top-left of the app window.
        if self.status_calls == 1:
            self.update_idletasks()
            self.titlebar_offset = toplevel.winfo_y() - self.winfo_y()

    def display_status(self, status_msg: str) -> None:
        """
        Pop-up a game status window to announce winner or tie with
        PvP and PvPC modes, or with a canceled autoplay.
        Provide option Buttons to play again or quit app.
        Play again option can be invoked with Return or Enter.
        Display tally of players' wins within a single play mode.

        :param status_msg: The status string to display in status window.
        :return: None
        """

        # Game result needs to be displayed, but first freeze game actions.
        self.unbind_game_board()
        self.quit_button.config(state=tk.DISABLED)
        self.disable('player_modes', 'auto_modes', 'auto_controls')

        self.whose_turn.set('Game pending...')
        self.whose_turn_lbl.config(bg=COLOR['tk_white'])

        # Need to update players' cumulative wins in the app window.
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        # Now set up the status window and its actions:
        status_window = tk.Toplevel(self,
                                    bg=COLOR['status_bg'],
                                    borderwidth=4,
                                    relief='raised')
        status_window.title('Game Status')

        if MY_OS == 'win':  # Windows
            size = '500x150'
            min_w = 300
            min_h = 150
        elif MY_OS == 'dar':  # macOS
            size = '200x90'
            min_w = 150
            min_h = 90
        else:  # Linux
            size = '230x100'
            min_w = 180
            min_h = 100

        status_window.geometry(size)
        status_window.minsize(min_w, min_h)

        self.status_calls += 1
        self.window_geometry(status_window)

        # Need to prevent focus shifting to app window which would cover
        #  the Report window.
        status_window.attributes('-topmost', True)
        status_window.focus_force()

        status_lbl = tk.Label(status_window,
                              text=status_msg,
                              font=FONT['status'],
                              bg=COLOR['status_bg'])

        def no_exit_on_x():
            messagebox.showinfo(
                parent=status_window,
                title='Click a button',
                detail='Use either "New Game" or "Quit"'
                       ' to close Report window.')

        status_window.protocol('WM_DELETE_WINDOW', no_exit_on_x)

        def restart_game():
            """
            Record current xy geometry of Report window, then reset game
            board and close window.
            Called from keybind and Button cmd.

            :return: None
            """

            # Need to retain screen position of status window between
            #   games in case user has moved it.
            self.statuswin_geometry = (
                f'+{status_window.winfo_x()}'
                f'+{status_window.winfo_y() - self.titlebar_offset}'
            )
            self.new_game()
            status_window.destroy()

        again = tk.Button(status_window, text='New Game (\u23CE)',
                          # Unicode Return/Enter key symbol ^^^.
                          font=FONT['button_bold'],
                          relief='groove',
                          overrelief='raised',
                          border=3,
                          command=restart_game)
        not_again = tk.Button(status_window, text='Quit',
                              font=FONT['button'],
                              relief='groove',
                              overrelief='raised',
                              border=3,
                              command=lambda: utils.quit_game(mainloop=self))
        status_window.bind('<Return>', lambda _: restart_game())
        status_window.bind('<KP_Enter>', lambda _: restart_game())

        status_lbl.pack(pady=3, padx=3)
        again.pack(pady=(0, 0))
        not_again.pack(pady=5)

    def new_game(self) -> None:
        """
        Set configurations for a new game.

        Called from display_status.restart_game().
        Calls to setup_game_board(); conditionally to ready_player_one(),
        utils.keybindings(), pc_turn(), reset_game_and_score().
        return: None
        """
        mode = self.mode_clicked.get()

        self.auto_random_mode.config(state=tk.NORMAL)
        self.auto_center_mode.config(state=tk.NORMAL)
        self.auto_tactics_mode.config(state=tk.NORMAL)
        self.autospeed_fast.config(state=tk.NORMAL)
        self.autospeed_slow.config(state=tk.NORMAL)

        self.pvp_mode.config(state=tk.NORMAL)
        self.pvpc_mode.config(state=tk.NORMAL)

        self.quit_button.config(state=tk.NORMAL)

        # Make font invisible (bg color) to remove from view.
        self.auto_turns_header.config(fg=COLOR['tk_white'])
        self.auto_turns_lbl.config(fg=COLOR['tk_white'])

        self.winner_found = False
        self.setup_game_board()

        if mode == 'pvp':
            utils.keybindings(self, 'bind_board')
            self.choose_pc_pref.config(state=tk.DISABLED)

            if self.prev_game_num.get() % 2 == 0:
                self.ready_player_one()
            else:
                self.whose_turn.set(f'{PLAYER2} plays {P2_MARK}')
                self.whose_turn_lbl.config(bg=COLOR['tk_white'])

        elif mode == 'pvpc':
            utils.keybindings(self, 'bind_board')

            if self.prev_game_num.get() % 2 != 0:
                self.whose_turn.set(f'PC plays {P2_MARK}')
                self.whose_turn_lbl.config(bg=COLOR['tk_white'])
                self.disable('auto_modes', 'auto_controls')
                self.pc_turn()
            else:
                self.ready_player_one()
                self.choose_pc_pref.config(state='readonly')

        # At restart of an autoplay series or when stopped by user,
        #   need to clear auto scores and games.
        elif 'Autoplay' in mode:
            self.reset_game_and_score()
            self.auto_turns_remaining.set(0)
            self.auto_marks = ''
            self.auto_start_stop_btn.config(text='Start Autoplay',
                                            state=tk.NORMAL)
            self.who_autostarts_btn.configure(state=tk.NORMAL)
            self.choose_pc_pref.config(state=tk.DISABLED)

    def reset_game_and_score(self) -> None:
        """
        Set game number and player points to zero.

        Called from mode_control() when user changes between PvP and
        PvPC or changes PvPC play mode, from new_game() when in Autoplay
        mode, from auto_start(), and from Combobox selection bindings.

        :return: None
        """
        self.prev_game_num.set(0)
        self.p1_score.set(0)
        self.p2_score.set(0)
        self.p1_points = 0
        self.p2_points = 0
        self.ties_num.set(0)
        self.setup_game_board()

        if 'Autoplay' in self.mode_clicked.get():
            self.unbind_game_board()
            self.whose_turn.set(self.curr_automode)
            self.whose_turn_lbl.config(bg=COLOR['tk_white'])

    def auto_command(self) -> None:
        """
        Manage on/off commands of auto_start_stop_btn Button.

        Toggles text displayed on auto_start_stop_btn.
        Calls to auto_start(), auto_stop().
        :return: None
        """
        if self.auto_start_stop_btn['text'] == 'Start Autoplay':

            if 'Autoplay' in self.mode_clicked.get():
                self.auto_start_stop_btn['text'] = 'Stop Autoplay'
                self.auto_start()
            else:
                self.auto_start_stop_btn['text'] = 'Start Autoplay'
        else:
            self.auto_start_stop_btn['text'] = 'Start Autoplay'
            self.auto_stop('canceled')

    def auto_start(self) -> None:
        """
        Set starting values for autoplay; call selected Autoplay method.

        Display number of auto turns remaining.
        Disable modes during autoplay.
        :return: None
        """
        self.auto_setup()
        self.reset_game_and_score()
        self.whose_turn.set(self.curr_automode)
        self.whose_turn_lbl.config(bg=COLOR['tk_white'])

        # Change font from invisible (bg color) to default color to view.
        self.auto_turns_header.config(fg='black')
        self.auto_turns_lbl.config(fg='black')

        self.auto_start_stop_btn.config(state=tk.NORMAL)
        self.who_autostarts_btn.config(state=tk.DISABLED)

        # Provide alternating pc player marks in autoplay turns;
        #   The marks string is shortened one character per turn in the
        #   autoplay_* methods, and in auto_setup() depending on the
        #   who_autostarts_btn option.
        self.auto_marks = ''.join(map(lambda m1, m2: m1 + m2, MARKS1, MARKS2))

        # Start repeating calls to one of the autoplay methods;
        #   calls are controlled by after_id.
        if self.mode_clicked.get() == 'Autoplay random':
            self.autoplay_random()
        elif self.mode_clicked.get() == 'Autoplay tactics':
            self.autoplay_tactics()
        elif self.mode_clicked.get() == 'Autoplay center':
            self.autoplay_center()

        # Do not allow mode selection while autoplay is in progress.
        #   Reset all to NORMAL or 'readonly' in new_game().
        self.disable('player_modes', 'auto_modes')

    def auto_stop(self, stop_msg: str) -> None:
        """
        Stop autoplay method and call Game Status popup window.

        Disable player game actions (actions enabled once Game Status
        window closes).

        :param stop_msg: Information on type of auto_stop call; e.g.,
            "ended", "cancelled", etc.
        :return: None
        """
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.setup_game_board()
        self.display_status(f'{self.curr_automode}, {stop_msg}')

    def auto_setup(self) -> None:
        """
        At start of new autoplay games, update scores in the main window.

        Clear all marks from the board.
        Called from auto_start() and auto_flash_game().

        :return: None
        """
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        if len(self.auto_marks) > 0:
            if self.who_autostarts_btn['text'] == 'Player 1 starts':
                # All games start with P1_MARK.
                self.auto_marks = self.auto_marks.lstrip(P2_MARK)
            else:
                # Games alternate starts between P1_MARK and P2_MARK.
                if self.prev_game_num.get() % 2 == 0:
                    self.auto_marks = self.auto_marks.lstrip(P2_MARK)
                else:
                    self.auto_marks = self.auto_marks.lstrip(P1_MARK)

        self.winner_found = False
        self.setup_game_board()

    def autostart_who(self) -> None:
        """
        Toggle who_autostarts_btn Button text.

        Button's text content is used for conditions in auto_setup().

        :return: None
        """
        if self.who_autostarts_btn['text'] == 'Player 1 starts':
            self.who_autostarts_btn['text'] = 'Players alternate'
        else:
            self.who_autostarts_btn['text'] = 'Player 1 starts'

    def autospeed_control(self, after_type='game') -> int:
        """
        Set after() times used in auto_flash_game() and Autoplay modes.

        Called from autospeed_fast and autospeed_slow Radiobuttons;
        from auto_flash_game() to set time for erasing flash color;
        from each autoplay_* method to set time between game restarts.
        The *after_type* param is used as a default argument for
        convenience of calling this method as a Radiobutton command.

        :param after_type: Function type to be paused; 'game' (default),
                          'flash', or 'fast'.
        :return: Milliseconds to use in after() calls.
        """

        if self.autospeed_selection.get() == 'fast':
            after_time = AUTO_FAST
        else:  # Is 'game' or 'flash' (or a misspelled argument call).
            after_time = AUTO_SLOW

        # Note: *after_type* 'flash' is called from auto_flash_game()
        #   where the flash time needs to be less than the after_time
        #   time; this allows proper operation of auto_flash_game().
        if after_type == 'flash':
            after_time = int(after_time * 0.9)

        return after_time

    def autoplay_random(self) -> None:
        """
        Play all turns at random positions in Autoplay mode.

        Number of turns is set by auto_marks, currently 1000 turns,
        which gives ~130 games or until stopped by user.
        Turns are played on a timed interval controlled by calls to
        auto_repeat().
        Yields ~15% tie games.
        Is called from auto_start().

        :return: None
        """
        self.curr_automode = 'Autoplay random'
        self.auto_turns_remaining.set(len(self.auto_marks))
        turn_number = self.turn_number()

        if len(self.auto_marks) > 0:
            mark = self.auto_marks[0]
            self.play_random(turn_number, mark)
            self.auto_repeat(mark, self.autoplay_random)
        else:
            self.auto_stop('ended')

    def autoplay_center(self) -> None:
        """
        First play is always at the center position.

        Subsequent play preference is : win, block, random.

        Number of turns is set by auto_marks, currently 1000 turns,
        which gives ~120 games or until stopped by user.
        Turns are played on a timed interval controlled by calls to
        auto_repeat().
        Yields ~60% tie games.
        Is called from auto_start().

        :return: None
        """
        self.curr_automode = 'Autoplay center'

        self.auto_turns_remaining.set(len(self.auto_marks))
        turn_number = self.turn_number()

        if len(self.auto_marks) > 0:
            mark = self.auto_marks[0]

            # Fill in the available center.
            if self.board_labels[4]['text'] == ' ':
                self.board_labels[4]['text'] = mark

            # Look for a winning or blocking play.
            if turn_number == self.turn_number():
                self.play_rudiments(mark)

            # No preferred play available, so play random.
            if turn_number == self.turn_number():
                self.play_random(turn_number, mark)

            self.auto_repeat(mark, self.autoplay_center)

        else:
            self.auto_stop('ended')

    def autoplay_tactics(self) -> None:
        """
        Auto-plays turns according to a set order of conditional rules.

        Rules, in decreasing play priority: win, block, defend against
        an opponent advantage, play corners for an advantage, random.
        Number of turns is set by auto_marks, currently 1000 turns,
        which gives ~100 games or until stopped by user.
        Turns are played on a timed interval controlled by calls to
        auto_repeat().
        Yields ~99% tie games.
        Is called from auto_start().

        :return: None
        """
        self.curr_automode = 'Autoplay tactics'

        self.auto_turns_remaining.set(len(self.auto_marks))
        turn_number = self.turn_number()

        if len(self.auto_marks) > 0:
            mark = self.auto_marks[0]

            # Need to randomize starting play so games don't always
            #  start with a corner play.
            if turn_number == 0:
                self.play_random(turn_number, mark)

            # Look for a winning or blocking play.
            if turn_number == self.turn_number():
                self.play_rudiments(mark)

            if turn_number == self.turn_number():
                self.play_defense(turn_number, mark)

            if turn_number == self.turn_number():
                self.play_corners(turn_number, mark)

            # No preferred play available, so play random.
            if turn_number == self.turn_number():
                self.play_random(turn_number, mark)

            self.auto_repeat(mark, self.autoplay_tactics)

        else:
            self.auto_stop('ended')

    def auto_repeat(self, mark: str, auto_method: Callable) -> None:
        """
        Complete and repeat each autoplay turn.

        Checks for winner, advances to the next player's *mark*, and
        applies after() to delay and repeat the *auto_method*.

        :param mark: The current played mark character.
        :param auto_method: The calling autoplay_* method.
        :return: None
        """

        if self.turn_number() >= 5:
            self.check_winner(mark)

        # Need to the advance the mark for next turn.
        self.auto_marks = self.auto_marks.lstrip(mark)

        # Need a pause so user can see what play was made and also
        #   allow auto_stop() to break the call cycle.
        self.after_id = self.after(self.autospeed_control('game'), auto_method)

    def auto_flash_game(self, combo: tuple, mark: str) -> None:
        """
        For each auto_play game, flashes the marks for win or tie.

        On ties, flashes the played board, then the center with 'TIE'
        On wins, flashes the winning marks.
        Timing is everything.
        Calls auto_setup() for the next auto_play() game.

        Derived from Bryan Oakley's answer for
        how-to-make-a-button-flash-using-after-in-tkinter
        https://stackoverflow.com/a/57298778
        :param combo: The tuple index values for the board_labels
                    squares to flash. For tie games call with (4, 4, 4).
        :param mark: The winning player's mark, usually 'X' or 'O'.
                     For tie games call with 'TIE'.
        """
        _x, _y, _z = combo

        def flash_show():
            self.board_labels[_x].config(text=mark, bg=COLOR['sq_won'])
            self.board_labels[_y].config(text=mark, bg=COLOR['sq_won'])
            self.board_labels[_z].config(text=mark, bg=COLOR['sq_won'])
            self.update_idletasks()

        def flash_erase():
            self.board_labels[_x].config(text=' ', bg=COLOR['sq_not_won'])
            self.board_labels[_y].config(text=' ', bg=COLOR['sq_not_won'])
            self.board_labels[_z].config(text=' ', bg=COLOR['sq_not_won'])

        # On a tie game, flash the board, then 'TIE' in center square.
        #   Flashing the board assures display of the last played *mark*.
        if mark == 'TIE':
            for lbl in self.board_labels:
                lbl.config(bg=COLOR['sq_won'])
                self.update_idletasks()
            self.after(self.autospeed_control('fast'))

        # after() time of 1ms is needed for the flash to work.
        self.after(1, flash_show)
        self.after(self.autospeed_control('flash'), flash_erase)

        # Need to allow idle time for auto_setup to complete given
        #   autospeed_control() time; keeps auto_marks in correct register.
        self.after_idle(self.auto_setup)

def run_checks() -> None:
    """
    Run checks on supported platforms and Python versions; exit on fail.

    :return: None
    """
    utils.check_platform()
    vcheck.minversion('3.7')

    # Check for invocation arguments (exit after running --about).
    utils.manage_args()

def main():
    app = TicTacToeGUI()
    app.title('TIC TAC TOE')
    app.resizable(False, False)

    # Developer: use custom handlers for unhandled system and tkinter exceptions.
    # sys.excepthook = utils.handle_exception
    # app.report_callback_exception = utils.handle_exception

    # Need an image to replace blank tk desktop icon.
    #   Set correct path to the local 'images' directory and icon file.
    try:
        icon_path = utils.valid_path_to('images/Tic_tac_toe.png')
        icon = tk.PhotoImage(file=icon_path)
        app.wm_iconphoto(True, icon)
    except tk.TclError as msg:
        print('Cannot display program icon, so it will be left blank or tk default.')
        print(f'tk error message: {msg}')

    print(f'{utils.program_name()} now running...')

    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\n*** User quit the program from Terminal/Console ***\n")

if __name__ == '__main__':

    run_checks() # Comment out to run PyInstaller on this script.
    main()

#!/usr/bin/env python3

"""
ttt.py is a tkinter GUI offering various play modes of the Tic Tac Toe
game. The objective is to win a game by getting three of your player's
marks (either X or O) in a row on a 3x3 game board.
Play mode options:
  Player v Player,
  Player v PC (with PC preference options),
  Autoplay, about 120 games of the PC playing itself in either random or
    strategic mode options and an optinon for either one Player always
    goes first or Players alternate the first turn.

Requires tkinter (tk/tcl) and Python3.6+.
Developed in Python 3.8-3.9 with tkinter 8.6.

Inspired by Riya Tendulkar code:
https://levelup.gitconnected.com/how-to-code-tic-tac-toe-in-python-using-tkinter-e7f9ce510bfb
https://gist.github.com/riya1620/72c2b668ef29da061c44d97a82318572
"""
# Copyright: (c) 2022 Craig S. Echt, under MIT License

import random
import sys

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except (ImportError, ModuleNotFoundError) as error:
    print(f'This program requires tkinter, which is included with \n'
          'Python 3.7+ distributions.\n'
          'Install the most recent version or re-install Python and include Tk/Tcl.\n'
          '\nLinux users may need this: $ sudo apt-get install python3-tk\n'
          f'See also: https://tkdocs.com/tutorial/install.html \n{error}')

from ttt_utils import utils, platform_check as chk


class TicTacToeGUI(tk.Tk):
    """
    Display the tkinter GUI playing board and its control buttons.
    Provide multi-mode play action, with scoring.
    Methods: configure_widgets, your_turn_player1, grid_widgets,
        setup_game_board, unbind_game_board, on_enter, on_leave,
        mode_control, human_turn, pc_turn, pc_plays_random, turn_number,
        check_winner, flash_win, flash_tie, window_geometry, display_report,
        block_all_player_action, new_game, reset_game_and_score,
        auto_command, auto_start, auto_stop, auto_setup, auto_turn_limit,
        autoplay_random, autoplay_strategy, auto_flash.
    """

    def __init__(self):
        super().__init__()

        self.player1 = 'PLAYER 1'
        self.player2 = 'PLAYER 2'
        self.p1_mark = 'X'  # Can use any utf-8 character
        self.p2_mark = 'O'
        self.p1_points = 0
        self.p2_points = 0
        self.p1_score = tk.IntVar()
        self.p2_score = tk.IntVar()
        self.winner_found = False
        self.prev_game_num_header = tk.Label()
        self.prev_game_num = tk.IntVar(value=0)
        self.prev_game_num_lbl = tk.Label()

        # Player's turn widgets.
        self.whose_turn = tk.StringVar()
        self.whose_turn_lbl = tk.Label()
        self.auto_turns_header = tk.Label()
        self.auto_turns_lbl = tk.Label()
        self.auto_turns_remaining = tk.IntVar()
        # auto_turns_remaining is set to length of autoplay_marks string.

        # Players' scores widgets.
        self.score_header = tk.Label()
        self.player1_header = tk.Label()
        self.player2_header = tk.Label()
        self.player1_score_lbl = tk.Label()
        self.player2_score_lbl = tk.Label()
        self.ties_header = tk.Label()
        self.ties_num = tk.IntVar(value=0)
        self.ties_lbl = tk.Label()

        # Play action widgets.
        self.board_labels = [tk.Label() for _ in range(9)]
        self.mode_selection = tk.StringVar()
        self.pvp_mode = tk.Radiobutton()
        self.pvpc_mode = tk.Radiobutton()
        self.choose_pc_pref = ttk.Combobox()
        self.auto_random_mode = tk.Radiobutton()
        self.auto_strategy_mode = tk.Radiobutton()
        self.autoplay_on = tk.BooleanVar()
        self.auto_go_stop_radiobtn = tk.Radiobutton()
        self.auto_go_stop_txt = tk.StringVar()
        self.who_autostarts = ttk.Button()

        self.quit_button = ttk.Button()

        # Additional widgets.
        self.separator = ttk.Separator()
        self.after_id = None
        self.play_after = 600  # ms, pause between turns in play PC mode.
        self.auto_after = 300  # ms, for autoplay turns and game turnovers.
        self.all_autoplay_marks = ''  # Used to dole out PC marks in proper order.
        self.curr_automode = ''  # Used to display whose_turn.
        self.curr_pmode = ''  # Used to evaluate conditions.
        self.report_geometry = ''
        self.report_calls = 0
        self.titlebar_offset = 0

        self.font = {}

        # Foreground and background colors.
        self.color = {'score_fg': 'DodgerBlue4',
                      'result_bg': 'yellow3',
                      'disabled_fg': 'grey65',
                      'tk_white': '',  # defined in configure_widgets()
                      'mark_fg': 'yellow2',
                      'sq_won': 'blue',
                      'sq_not_won': 'black',
                      'sq_mouseover': 'grey15',
                      'radiobtn_bg': 'DodgerBlue1',
                      }

        self.configure_widgets()
        self.grid_widgets()

    def configure_widgets(self) -> None:
        """Initial configurations of app window widgets."""
        ttk.Style().theme_use('alt')

        self.font['sm_button'] = ('TkHeadingFont', 8)
        self.font['who'] = ('TkHeadingFont', 7, 'italic bold')
        self.font['button'] = ('TkHeadingFont', 8, 'bold')
        self.font['scores'] = ('TkHeadingFont', 9)
        self.font['report'] = ('TkHeadingFont', 9, 'italic bold')
        self.font['condensed'] = ('TkTooltipFont', 8)
        self.font['mark'] = ('TkFixedFont', 50)

        # Need to apply OS-specific adjustments.
        if chk.MY_OS == 'lin':
            self.font['report'] = ('TkHeadingFont', 10, 'italic bold')
        elif chk.MY_OS == 'dar':
            self.font['sm_button'] = ('TkHeadingFont', 10)
            self.font['who'] = ('TkHeadingFont', 11, 'italic bold')
            self.font['button'] = ('TkHeadingFont', 10, 'bold')
            self.font['scores'] = ('TkHeadingFont', 12)
            self.font['condensed'] = ('TkTooltipFont', 10)

        if chk.MY_OS == 'dar':
            self.color['tk_white'] = 'white'
        elif chk.MY_OS == 'lin':
            self.color['tk_white'] = 'grey85'
        elif chk.MY_OS == 'win':
            self.color['tk_white'] = 'grey95'

        # Player's turn widgets.
        self.prev_game_num_header.config(text='Games played',
                                         font=self.font['condensed'])
        self.prev_game_num_lbl.config(textvariable=self.prev_game_num,
                                      font=self.font['condensed'])
        self.whose_turn_lbl.config(textvariable=self.whose_turn, height=4,
                                   font=self.font['who'])
        self.your_turn_player1()

        self.auto_turns_header.config(text='Turns to go',
                                      font=self.font['condensed'])
        self.auto_turns_lbl.config(textvariable=self.auto_turns_remaining,
                                   font=self.font['condensed'])

        # Players' scores widgets:
        # ︴symbol from https://coolsymbol.com/line-symbols.html
        self.score_header.config(
            text='Score ︴', font=self.font['scores'],
            fg=self.color['score_fg'])
        self.player1_header.config(
            text='Player 1:', font=self.font['scores'],
            fg=self.color['score_fg'])
        self.player2_header.config(
            text='Player 2:', font=self.font['scores'],
            fg=self.color['score_fg'])
        self.player1_score_lbl.config(
            textvariable=self.p1_score, font=self.font['scores'],
            fg=self.color['score_fg'])
        self.player2_score_lbl.config(
            textvariable=self.p2_score, font=self.font['scores'],
            fg=self.color['score_fg'])
        self.ties_header.config(
            text='Ties:', font=self.font['scores'],
            fg=self.color['score_fg'])
        self.ties_lbl.config(
            textvariable=self.ties_num, font=self.font['scores'],
            fg=self.color['score_fg'])

        # Play mode control widgets:
        self.pvp_mode.config(text='Player v Player',
                             font=self.font['condensed'],
                             variable=self.mode_selection,
                             value='pvp',
                             command=self.mode_control)
        self.pvp_mode.select()

        self.pvpc_mode.config(text='Player v PC',
                              font=self.font['condensed'],
                              variable=self.mode_selection,
                              value='pvpc',
                              command=self.mode_control)

        # choose_pc_pref is enabled as readonly when pvpc_mode is selected.
        #   Set drop-down list font size to match displayed font size.
        #   Set random, 1st in tuple, as the default.
        self.choose_pc_pref.config(font=self.font['condensed'],
                                   width=14,
                                   values=('PC plays random',
                                           'PC plays corners',
                                           'PC plays center',
                                           'PC plays strategy'),
                                   state=tk.DISABLED)
        self.option_add("*TCombobox*Font", self.font['condensed'])
        if chk.MY_OS == 'dar':
            self.choose_pc_pref.config(width=13)
        self.choose_pc_pref.current(0)
        self.choose_pc_pref.bind('<<ComboboxSelected>>',
                                 lambda _: self.reset_game_and_score())

        self.separator.configure(orient='horizontal')

        self.auto_random_mode.config(text='Autoplay random',
                                     font=self.font['condensed'],
                                     variable=self.mode_selection,
                                     value='auto-random',
                                     command=self.mode_control)
        self.auto_strategy_mode.config(text='Autoplay strategy',
                                       font=self.font['condensed'],
                                       variable=self.mode_selection,
                                       value='auto-strategy',
                                       command=self.mode_control)
        self.auto_go_stop_radiobtn.config(textvariable=self.auto_go_stop_txt,
                                          font=self.font['button'],
                                          variable=self.autoplay_on,
                                          fg=self.color['mark_fg'],
                                          bg=self.color['radiobtn_bg'],
                                          borderwidth=2,
                                          indicatoron=False,
                                          command=self.auto_command)
        self.auto_go_stop_txt.set('Start autoplay')
        self.auto_go_stop_radiobtn.config(state=tk.DISABLED)

        # ttk.Buttons are used b/c tk.Buttons cannot be configured in macOS.
        style = ttk.Style()
        style.map('My.TButton',
                  foreground=[('pressed', self.color['disabled_fg']),
                              ('active', self.color['mark_fg']),
                              ('disabled', self.color['disabled_fg'])
                              ],
                  background=[('pressed', self.color['tk_white']),
                              ('active', self.color['radiobtn_bg'])],
                  )
        style.configure('My.TButton', font=self.font['sm_button'])
        self.who_autostarts.configure(style="My.TButton",
                                      text='Player 1 starts', width=14,
                                      state=tk.DISABLED,
                                      takefocus=False,
                                      command=self.set_who_autostarts)

        self.quit_button.config(style="My.TButton",
                                text='Quit', width=4,
                                command=utils.quit_game)

        # Configure game board play squares:
        self.setup_game_board()

    def grid_widgets(self) -> None:
        """Position app window widgets."""

        # Position play action Labels in 3 x 3 grid. Note that while
        #   nothing is gridded in row index 1, the top row uses rowspan=2
        #   to center widgets vertically; hence, board_labels begin on
        #   row index 2.
        _row = 2
        _col = 0
        for lbl in self.board_labels:
            # if chk.MY_OS in 'win, dar':
            if chk.MY_OS == 'dar':
                lbl.grid(row=_row, column=_col, pady=6, padx=6, ipady=6, ipadx=10)
            elif chk.MY_OS == 'win':
                lbl.grid(row=_row, column=_col, pady=6, padx=6, ipady=6, ipadx=10)
            else:  # Linux (lin)
                lbl.grid(row=_row, column=_col, pady=1, padx=1, ipady=6, ipadx=10)
            _col += 1
            if _col > 2:
                _col = 0
                _row += 1

        # Squeeze everything in with pretty spanning, padding, and stickies.
        #  Grid statements are sorted by row, then column.
        # self.rowconfigure(0, minsize=80)
        self.whose_turn_lbl.grid(  # padx matches that of board_labels.
            row=0, column=0, padx=0, pady=(5, 0))
        self.prev_game_num_header.grid(
            row=0, column=2, rowspan=2, padx=(0, 8), pady=(5, 0), sticky=tk.NE)
        self.prev_game_num_lbl.grid(
            row=0, column=2, rowspan=2, padx=(0, 8), pady=(24, 0), sticky=tk.NE)
        if chk.MY_OS == 'win':
            self.prev_game_num_header.grid(
                row=0, column=2, rowspan=2, padx=(0, 8), pady=(10, 0), sticky=tk.NE)
            self.prev_game_num_lbl.grid(
                row=0, column=2, rowspan=2, padx=(0, 8), pady=(35, 0), sticky=tk.NE)

        # There is duplication in the elif statements to allow easy editing and
        #  cut/paste options for platform-specific needs.
        if chk.MY_OS == 'dar':
            self.score_header.grid(
                row=0, column=1, rowspan=2, padx=(10, 0), pady=(0, 10), sticky=tk.W)
            self.player1_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 0), pady=(0, 40), sticky=tk.E)
            self.player2_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 0), pady=(20, 10), sticky=tk.E)
        elif chk.MY_OS == 'lin':
            self.score_header.grid(
                row=0, column=1, rowspan=2, padx=(10, 0), pady=(0, 10), sticky=tk.W)
            self.player1_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(0, 40), sticky=tk.E)
            self.player2_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(20, 10), sticky=tk.E)
        elif chk.MY_OS == 'win':
            self.score_header.grid(
                row=0, column=1, rowspan=2, padx=(10, 0), pady=(0, 10), sticky=tk.W)
            self.player1_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(0, 50), sticky=tk.E)
            self.player2_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(30, 10), sticky=tk.E)

        self.player1_score_lbl.grid(
            row=0, column=2, rowspan=2, padx=0, pady=(0, 40), sticky=tk.W)
        self.player2_score_lbl.grid(
            row=0, column=2, rowspan=2, padx=0, pady=(20, 10), sticky=tk.W)
        if chk.MY_OS == 'win':
            self.player1_score_lbl.grid(
                row=0, column=2, rowspan=2, padx=0, pady=(0, 50), sticky=tk.W)
            self.player2_score_lbl.grid(
                row=0, column=2, rowspan=2, padx=0, pady=(30, 10), sticky=tk.W)

        # Auto-turn counting labels are gridded in auto_start().

        self.ties_header.grid(
            row=0, column=1, rowspan=2, padx=(0, 8), pady=(55, 0), sticky=tk.E)
        self.ties_lbl.grid(
            row=0, column=2, rowspan=2, padx=0, pady=(55, 0), sticky=tk.W)
        if chk.MY_OS == 'win':
            self.ties_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(85, 0), sticky=tk.E)
            self.ties_lbl.grid(
                row=0, column=2, rowspan=2, padx=0, pady=(85, 0), sticky=tk.W)

        self.pvp_mode.grid(
            row=5, column=0, padx=(10, 0), pady=5, sticky=tk.W)
        if chk.MY_OS == 'dar':
            self.pvpc_mode.grid(
                row=5, column=1, columnspan=2, padx=(20, 0), pady=5, sticky=tk.W)
            self.choose_pc_pref.grid(
                row=5, column=1, columnspan=2, padx=(0, 25), pady=0, sticky=tk.E)
        else:
            self.pvpc_mode.grid(
                row=5, column=1, columnspan=2, padx=(0, 0), pady=5, sticky=tk.W)
            self.choose_pc_pref.grid(
                row=5, column=1, columnspan=2, padx=(0, 35), pady=0, sticky=tk.E)

        self.separator.grid(
            row=7, column=0, columnspan=3, padx=10, sticky=tk.EW)

        self.auto_random_mode.grid(
            row=8, column=0, padx=0, pady=(4, 0), sticky=tk.W)
        self.auto_go_stop_radiobtn.grid(
            row=8, column=1, rowspan=2, padx=0, pady=(12, 0), sticky=tk.EW)

        self.auto_strategy_mode.grid(
            row=9, column=0, padx=0, pady=0, sticky=tk.W)

        self.who_autostarts.grid(
            row=10, column=0, padx=(15, 0), pady=5, sticky=tk.W)
        self.quit_button.grid(
            row=10, column=2, padx=5, pady=(0, 5), sticky=tk.E)

    def setup_game_board(self) -> None:
        """
        Configure and activate play action for the game board squares.

        :return: None
        """
        for i, lbl in enumerate(self.board_labels):
            lbl.config(text=' ', height=1, width=2,
                       bg=self.color['sq_not_won'], fg=self.color['mark_fg'],
                       font=self.font['mark'],

                       )
            if chk.MY_OS == 'dar':
                lbl.config(borderwidth=12)
            else:
                lbl.config(highlightthickness=6)

            lbl.bind('<Button-1>', lambda event, lbl_idx=i: self.human_turn(
                self.board_labels[lbl_idx]))
            lbl.bind('<Enter>', lambda event, l=lbl: self.on_enter(l))
            lbl.bind('<Leave>', lambda event, l=lbl: self.on_leave(l))

    def unbind_game_board(self) -> None:
        """
        Prevent user action on game board squares.

        :return: None
        """
        for lbl in self.board_labels:
            lbl.unbind('<Button-1>')
            lbl.unbind('<Enter>')
            lbl.unbind('<Leave>')

    def on_enter(self, label: tk) -> None:
        """
        On mouseover, indicate game board square with a color change.

        :param label: The tk.Label object.
        :return: None
       """
        if label['bg'] == self.color['sq_not_won']:
            label['bg'] = self.color['sq_mouseover']
        elif label['bg'] == self.color['sq_won']:
            label['bg'] = self.color['sq_won']

    def on_leave(self, label: tk):
        """
        On mouse leave, game board square returns to entered color.

        :param label: The tk.Label object.
        :return: None
        """
        if label['bg'] == self.color['sq_mouseover']:
            label['bg'] = self.color['sq_not_won']
        elif label['bg'] == self.color['sq_not_won']:
            label['bg'] = self.color['sq_not_won']
        elif label['bg'] == self.color['sq_won']:
            label['bg'] = self.color['sq_won']

    def mode_control(self) -> None:
        """
        Block any mode change if in the middle of a game or autoplay.
        Disable and enable Radiobuttons as each mode requires.
        Cancel/ignore an errant or mistimed play mode selection.
        Is callback from the play mode Radiobuttons.

        :return: None
        """
        mode = self.mode_selection.get()
        # If a game is in progress, ignore any mode selections & post msg.
        if self.turn_number() > 0:
            if self.autoplay_on.get():
                if mode == 'auto-random':
                    self.auto_random_mode.deselect()
                elif mode == 'auto-strategy':
                    self.auto_strategy_mode.deselect()
                elif mode == 'pvp':
                    self.pvp_mode.deselect()
                elif mode == 'pvpc':
                    self.pvpc_mode.deselect()

                detail = ('Wait for autoplay to finish,\n'
                          'or click Stop autoplay button.')
                self.whose_turn.set(self.curr_automode)

            else:
                if self.curr_pmode == 'pvp':
                    self.pvp_mode.select()
                    self.choose_pc_pref.config(state=tk.DISABLED)
                    self.pvpc_mode.deselect()
                    self.auto_random_mode.deselect()
                    self.auto_strategy_mode.deselect()
                elif self.curr_pmode == 'pvpc':
                    self.pvpc_mode.select()
                    self.choose_pc_pref.config(state='readonly')
                    self.pvp_mode.deselect()
                    self.auto_random_mode.deselect()
                    self.auto_strategy_mode.deselect()

                detail = 'Finish the current game,\nthen change mode.'

            messagebox.showinfo(title='Mode is unavailable now',
                                detail=detail)

        else:  # No game in progress.
            self.reset_game_and_score()

            if mode == 'pvpc':
                self.choose_pc_pref.config(state='readonly')
            else:
                self.choose_pc_pref.config(state=tk.DISABLED)

            if mode in 'pvp, pvpc':
                self.auto_go_stop_radiobtn.config(state=tk.DISABLED)
                self.who_autostarts.configure(state=tk.DISABLED)
            else:
                self.auto_go_stop_radiobtn.config(state=tk.NORMAL)
                self.who_autostarts.configure(state=tk.NORMAL)

            if mode in 'auto-random, auto-strategy':
                self.whose_turn.set('PC autoplay')
                self.whose_turn_lbl.config(bg=self.color['tk_white'])
            else:
                self.your_turn_player1()

    def your_turn_player1(self) -> None:
        """
        Display when it is Player 1's turn to play.

        :return: None
        """
        # Need to inform player when it's their turn after PC has played.
        if self.mode_selection.get() == 'pvpc' and self.turn_number() == 1:
            self.whose_turn.set(f'PC played {self.p2_mark}\n'
                                f'Your turn {self.player1}')
        else:
            self.whose_turn.set(f'{self.player1} plays {self.p1_mark}')

        self.whose_turn_lbl.config(bg=self.color['result_bg'])

    def human_turn(self, played_lbl: tk) -> None:
        """
        Check whether *played_lbl* (game board square Label) selected by
        player was already played. If not, assign player's mark to the
        text value of the selected label.
        In Player v Player mode, player's alternate who plays first in
        consecutive games.
        In Player v PC mode, Player 1 (human) always has the first turn.
        Evaluate played squares for a win after the 5th turn.

        :param played_lbl: The tk.Label object that was clicked.
        :return: None
        """

        # At app start, Previous game # = 0, then increments after a win/tie.
        #  At start of a new game, turn # = 0.
        #  On even PvPC games, pc will have already played 1st turn.
        def h_plays_p1():
            played_lbl['text'] = self.p1_mark
            self.whose_turn.set(f'{self.player2} plays {self.p2_mark}')
            self.whose_turn_lbl.config(bg=self.color['tk_white'])

        def h_plays_p2():
            played_lbl['text'] = self.p2_mark
            played_lbl.config(fg=self.color['tk_white'])
            self.your_turn_player1()

        def h_plays_p1_v_pc():
            played_lbl['text'] = self.p1_mark
            self.whose_turn_lbl.config(bg=self.color['tk_white'])
            self.whose_turn.set(f'PC plays {self.p2_mark}')

        if played_lbl['text'] == ' ':
            if self.mode_selection.get() == 'pvp':
                self.curr_pmode = 'pvp'
                if self.prev_game_num.get() % 2 == 0:
                    if self.turn_number() % 2 == 0:
                        h_plays_p1()  # even prev_game, even turn
                    else:
                        h_plays_p2()  # even prev_game, odd turn
                else:
                    if self.turn_number() % 2 == 0:
                        h_plays_p2()  # odd prev_game, even turn
                    else:
                        h_plays_p1()  # odd prev_game, odd turn

                if self.turn_number() >= 5:
                    self.check_winner(played_lbl.cget('text'))

            elif self.mode_selection.get() == 'pvpc':
                self.curr_pmode = 'pvpc'
                if (self.turn_number() % 2 == 0 and
                        self.prev_game_num.get() % 2 == 0):
                    h_plays_p1_v_pc()  # even prev_game, even turn

                elif (self.turn_number() % 2 != 0 and
                      self.prev_game_num.get() % 2 != 0):
                    h_plays_p1_v_pc()  # odd prev_game, odd turn

                # Need update for app.after delay to work in pc_turn().
                app.update_idletasks()

                if self.turn_number() >= 5:
                    self.check_winner(self.p1_mark)

                if self.turn_number() < 9 and not self.winner_found:
                    self.pc_turn()
        else:
            messagebox.showerror('Oops!', 'This square was already played!')

        self.quit_button.config(command=lambda: utils.quit_game(False))

    def color_the_mark(self, _id: int) -> None:
        """
        In pvpc mode, when  played by the PC, provide an alternate to
        the default fg color for the played square (Label text), which
        is identified by the board_labels' index, *_id*.

        :param _id: The board label's list index of the played square.
        :return: None
        """
        # Note that the label fg in pvp mode is configured in
        #    human_turn.h_plays_p2().
        if not self.curr_automode:
            self.board_labels[_id].config(fg=self.color['tk_white'])

    def pc_turn(self) -> None:
        """
        Computer plays as Player2.
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
        #   that just delays closing the Result toplevel for a new game.
        if turn_number > 0:
            app.after(self.play_after)

        winning_combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),  # diagonals
        ]
        # Need to reorder list so Human doesn't detect a pattern of where PC will play.
        random.shuffle(winning_combos)

        corners = [0, 2, 6, 8]
        random.shuffle(corners)

        # Loops break with the first p2_mark played.
        while turn_number == self.turn_number():

            # Preference: all PC moves are random.
            if self.choose_pc_pref.get() == 'PC plays random':
                self.pc_plays_random(turn_number, self.p2_mark)

            # Preference: play the center when it is available.
            elif self.choose_pc_pref.get() == 'PC plays center':
                if self.board_labels[4]['text'] == ' ':
                    self.board_labels[4]['text'] = self.p2_mark
                    self.color_the_mark(4)

            # Start here when playing 'strategically' or 'prefers corners'.
            # Play for win.
            if turn_number == self.turn_number():
                for combo in winning_combos:
                    _x, _y, _z = combo
                    x_txt = self.board_labels[_x]['text']
                    y_txt = self.board_labels[_y]['text']
                    z_txt = self.board_labels[_z]['text']
                    if x_txt == y_txt == self.p2_mark and z_txt == ' ':
                        self.board_labels[_z]['text'] = self.p2_mark
                        self.color_the_mark(_z)
                        break
                    if y_txt == z_txt == self.p2_mark and x_txt == ' ':
                        self.board_labels[_x]['text'] = self.p2_mark
                        self.color_the_mark(_x)
                        break
                    if x_txt == z_txt == self.p2_mark and y_txt == ' ':
                        self.board_labels[_y]['text'] = self.p2_mark
                        self.color_the_mark(_y)
                        break

            # Play to block
            if turn_number == self.turn_number():
                for combo in winning_combos:
                    _x, _y, _z = combo
                    x_txt = self.board_labels[_x]['text']
                    y_txt = self.board_labels[_y]['text']
                    z_txt = self.board_labels[_z]['text']

                    if x_txt == y_txt == self.p1_mark and z_txt == ' ':
                        self.board_labels[_z]['text'] = self.p2_mark
                        self.color_the_mark(_z)

                        break
                    if y_txt == z_txt == self.p1_mark and x_txt == ' ':
                        self.board_labels[_x]['text'] = self.p2_mark
                        self.color_the_mark(_x)
                        break
                    if x_txt == z_txt == self.p1_mark and y_txt == ' ':
                        self.board_labels[_y]['text'] = self.p2_mark
                        self.color_the_mark(_y)
                        break

            # Prefer corners, as optioned.
            if self.choose_pc_pref.get() == 'PC plays corners':
                for _c in corners:
                    c_txt = self.board_labels[_c]['text']
                    if turn_number == self.turn_number() and c_txt == ' ':
                        self.board_labels[_c]['text'] = self.p2_mark
                        self.color_the_mark(_c)
                        break

            # If no block, win or preferred corner, then play random.
            if turn_number == self.turn_number():
                self.pc_plays_random(turn_number, self.p2_mark)

        if self.turn_number() >= 5:
            self.check_winner(self.p2_mark)

        self.your_turn_player1()

        app.update_idletasks()

    def pc_plays_random(self, turn_number: int, mark: str) -> None:
        """ All PC plays are to random positions.

        :param mark: The player's mark string to play.
        :param turn_number: The current turn number, from turn_number().
        :return: None
        """
        while turn_number == self.turn_number():
            random_idx = random.randrange(0, 9)
            if self.board_labels[random_idx]['text'] == ' ':
                self.board_labels[random_idx]['text'] = mark
                self.color_the_mark(random_idx)

    def turn_number(self) -> int:
        """
        Keep count of turns per game by counting play labels with
        a mark string as the label text.

        :return: The number of turns played, as integer.
         """
        turn = 0
        for lbl in self.board_labels:
            if lbl['text'] != ' ':
                turn += 1

        return turn

    def check_winner(self, mark: str) -> None:
        """
        Check each player's played mark (board_labels's text value) and
        evaluate whether played marks match a positional win in the
        board matrix (based on board_labels index values).

        :param mark: The played mark character to check for a win.
        :return: None
        """
        winning_combos = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),  # diagonals
        )

        def award_points(winning_mark):
            if winning_mark == self.p1_mark:
                self.p1_points += 1
            else:
                self.p2_points += 1

        # Loop breaks when the first winning combo is found.
        for combo in winning_combos:
            _x, _y, _z = combo
            lbl_x_txt = self.board_labels[_x]['text']
            lbl_y_txt = self.board_labels[_y]['text']
            lbl_z_txt = self.board_labels[_z]['text']

            if lbl_x_txt == lbl_y_txt == lbl_z_txt == mark:
                self.winner_found = True
                self.prev_game_num.set(self.prev_game_num.get() + 1)

                if self.mode_selection.get() in 'auto-random, auto-strategy':
                    award_points(mark)
                    self.auto_flash(combo, mark)
                    break

                # Mode selection is pvp or pvpc.
                award_points(mark)
                self.flash_win(combo)
                self.display_report(f'{mark} WINS!')
                break

        if self.turn_number() == 9 and not self.winner_found:
            self.winner_found = True
            self.prev_game_num.set(self.prev_game_num.get() + 1)

            self.p1_points += 0.5
            self.p2_points += 0.5

            self.ties_num.set(self.ties_num.get() + 1)

            if self.mode_selection.get() in 'auto-random, auto-strategy':
                self.auto_flash((4, 4, 4), 'TIE')
            else:
                self.flash_tie()
                self.display_report('IT IS A TIE!')

    def flash_win(self, combo) -> None:
        """
        Flashes the three winning squares, in series.
        Based on Bryan Oakley's answer for
        how-to-make-a-button-flash-using-after-in-tkinter
        https://stackoverflow.com/a/57298778

        :return: None
        """
        _x, _y, _z = combo

        app.after(10, lambda: self.board_labels[_x].config(bg=self.color['sq_won']))
        app.after(200, lambda: self.board_labels[_y].config(bg=self.color['sq_won']))
        app.after(400, lambda: self.board_labels[_z].config(bg=self.color['sq_won']))

    def flash_tie(self) -> None:
        """Make entire game board blue on a tied game.

        :return: None
        """
        for lbl in self.board_labels:
            lbl.config(bg=self.color['sq_won'])
            app.update_idletasks()

    def window_geometry(self, toplevel: tk) -> None:
        """
        Set the xy geometry of a *toplevel* window in top-left corner of
        app widget. If it is moved, then put at the new geometry
        determined by the report_geometry variable.
        Calculate the height of the system's window title bar to use as
        a y-offset for the *toplevel* xy geometry.

        :param toplevel: The tkinter toplevel object to position.
        :return: None
        """
        if self.report_geometry:
            toplevel.geometry(self.report_geometry)
        else:  # Set the initial xy position.
            toplevel.geometry(f'+{app.winfo_x()}+{app.winfo_y()}')

        # Need to position the geometry of the Report window by applying
        #   a y offset for the height of the system's window title bar.
        #   This is needed because tkinter widget geometry does not
        #   include the system's title bar.
        # Title bar height is determined only once from the initial
        #   placement of the Report window at top-left of the app window.
        if self.report_calls == 1:
            app.update_idletasks()
            self.titlebar_offset = toplevel.winfo_y() - app.winfo_y()

    def display_report(self, win_msg: str) -> None:
        """
        Pop-up a Game Report window to announce winner or tie with
        PvP and PvPC modes, or with a canceled autoplay.
        Provide option Buttons to play again or quit app.
        Play again option can be invoked with Return or Enter.
        Display tally of players' wins within a single play mode.

        :param win_msg: The result string to display in result window.
        :return: None
        """
        report_window = tk.Toplevel(self, borderwidth=4, relief='raised')
        report_window.title('TTT')
        report_window.config(bg=self.color['result_bg'])

        self.report_calls += 1
        self.window_geometry(report_window)

        # Need prevent focus shifting to app window which would cover up
        #  the Report window.
        report_window.attributes('-topmost', True)
        report_window.focus_force()

        if chk.MY_OS == 'dar':
            report_window.minsize(180, 80)
        elif chk.MY_OS == 'win':
            report_window.minsize(180, 80)
        elif chk.MY_OS == 'lin':
            report_window.minsize(150, 90)

        report_lbl = tk.Label(report_window, text=win_msg,
                              font=self.font['report'],
                              bg=self.color['result_bg'])

        self.block_all_player_action()
        self.whose_turn.set('Game pending...')
        self.whose_turn_lbl.config(bg=self.color['tk_white'])

        # Need to update players' cumulative wins in the app window.
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        def no_exit_on_x():
            messagebox.showinfo(
                parent=report_window,
                title='Click a button',
                detail='Use either "New Game" or "Quit"'
                       ' to close Report window.')

        report_window.protocol('WM_DELETE_WINDOW', no_exit_on_x)

        def restart_game():
            """
            Record current xy geometry of Report window, reset game
            board, then close window. Called from keybind and Button cmd.

            :return: None
            """
            self.report_geometry = (
                f'+{report_window.winfo_x()}'
                f'+{report_window.winfo_y() - self.titlebar_offset}'
            )
            self.new_game()
            report_window.destroy()

        again = tk.Button(report_window, text='New Game (\u23CE)',  # Return symbol.
                          font=self.font['button'],
                          relief='groove', overrelief='raised', border=3,
                          command=restart_game)
        not_again = tk.Button(report_window, text='Quit',
                              font=self.font['sm_button'],
                              relief='groove', overrelief='raised', border=3,
                              command=utils.quit_game)
        report_window.bind('<Return>', lambda _: restart_game())
        report_window.bind('<KP_Enter>', lambda _: restart_game())

        report_lbl.pack(pady=3, padx=3)
        again.pack(pady=(0, 0))
        not_again.pack(pady=5)

    def block_all_player_action(self) -> None:
        """
        Prevent user action in app window while Game Report window is
        open. Called from display_report().

        :return: None
        """
        self.unbind_game_board()
        self.quit_button.config(state=tk.DISABLED)
        self.auto_go_stop_radiobtn.config(state=tk.DISABLED)

    def new_game(self) -> None:
        """
        Set up the next game. Called from display_report().

        return: None
        """
        self.quit_button.config(state=tk.NORMAL, command=utils.quit_game)
        self.auto_go_stop_txt.set('Start autoplay')
        self.auto_go_stop_radiobtn.config(state=tk.NORMAL)

        self.auto_turns_header.grid_remove()
        self.auto_turns_lbl.grid_remove()

        self.setup_game_board()
        self.winner_found = False

        if self.mode_selection.get() == 'pvp':
            if self.prev_game_num.get() % 2 == 0:
                self.your_turn_player1()
            else:
                self.whose_turn.set(f'{self.player2} plays {self.p2_mark}')
                self.whose_turn_lbl.config(bg=self.color['tk_white'])

        elif self.mode_selection.get() == 'pvpc':
            if self.prev_game_num.get() % 2 != 0:
                self.whose_turn.set(f'PC plays {self.p2_mark}')
                self.whose_turn_lbl.config(bg=self.color['tk_white'])

                self.pc_turn()
            else:
                self.your_turn_player1()

        # At the end of an autoplay series or when stopped by user, need
        #   to clear auto scores and games.
        if ('Autoplay' in self.curr_automode or
                self.auto_turns_remaining.get() > 0):
            self.reset_game_and_score()
            self.curr_automode = ''
            self.auto_turns_remaining.set(0)
            self.all_autoplay_marks = ''

    def reset_game_and_score(self) -> None:
        """
        Set game number and player points to zero.
        Called from mode_control() when user changes between PvP and
        PvPC or changes PvPC play mode, and from auto_start(),
        new_game(), and Combobox selection binding.

        :return: None
        """
        self.prev_game_num.set(0)
        self.p1_score.set(0)
        self.p2_score.set(0)
        self.p1_points = 0
        self.p2_points = 0
        self.ties_num.set(0)
        self.your_turn_player1()
        self.setup_game_board()

    def auto_command(self) -> None:
        """
        Check that an autoplay mode is selected before calling
        auto_start() when the auto_go_stop_radiobtn Radiobutton invoked.
        Called as the auto_go_stop_radiobtn command.

        :return: None
        """
        if 'Start' in self.auto_go_stop_txt.get():
            if self.mode_selection.get() in 'auto-random, auto-strategy':
                self.auto_go_stop_txt.set('Stop autoplay')
                self.autoplay_on.set(True)
                self.auto_start()
            else:
                self.auto_go_stop_txt.set('Start autoplay')
                self.autoplay_on.set(False)

        else:
            self.auto_go_stop_txt.set('Start autoplay')
            self.autoplay_on.set(False)
            self.auto_stop('canceled')

    def auto_start(self) -> None:
        """
        Set starting values for autoplay and disable game modes when
        autoplay is in progress. Display number of auto turns remaining.

        :return: None
        """
        self.setup_game_board()
        self.reset_game_and_score()
        self.whose_turn.set('PC autoplay')
        self.whose_turn_lbl.config(bg=self.color['tk_white'])

        self.auto_turns_header.grid(row=0, column=2, rowspan=2,
                                    padx=(0, 8), pady=(0, 20), sticky=tk.SE)
        self.auto_turns_lbl.grid(row=0, column=2, rowspan=2,
                                 padx=(0, 8), pady=(0, 0), sticky=tk.SE)
        if chk.MY_OS == 'win':
            self.auto_turns_header.grid(row=0, column=2, rowspan=2,
                                        padx=(0, 8), pady=(0, 25), sticky=tk.SE)

        self.auto_go_stop_radiobtn.config(state=tk.NORMAL)
        self.who_autostarts.config(state=tk.DISABLED)

        self.auto_turn_limit()
        self.auto_setup()

        # Start repeating calls to one of the autoplay methods;
        #   calls are controlled by after_id.
        if self.mode_selection.get() == 'auto-random':
            self.autoplay_random()
        elif self.mode_selection.get() == 'auto-strategy':
            self.autoplay_strategy()

    def auto_stop(self, stop_msg: str) -> None:
        """
        Stop autoplay method and call Results popup window.
        Disable player game actions (resets when Results window closes).

        :param stop_msg: Information on source of auto_stop call.
        :return: None
        """
        if self.after_id:
            app.after_cancel(self.after_id)
            self.after_id = None

        self.who_autostarts.config(state=tk.NORMAL)

        self.setup_game_board()
        self.display_report(f'{self.curr_automode}, {stop_msg}')

    def auto_setup(self) -> None:
        """
        Run at the start of every new autoplay game. Update cumulative
        scores in the app window. Clear all marks from the board.
        Called from auto_start() and auto_flash().

        :return: None
        """
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        self.winner_found = False
        if len(self.all_autoplay_marks) > 0:
            if self.who_autostarts['text'] == 'Player 1 starts':
                # All games start with p1_mark.
                self.all_autoplay_marks = self.all_autoplay_marks.lstrip(self.p2_mark)
            else:
                # Games alternate starts between p1_mark and p2_mark.
                if self.prev_game_num.get() % 2 == 0:
                    self.all_autoplay_marks = self.all_autoplay_marks.lstrip(self.p2_mark)
                else:
                    self.all_autoplay_marks = self.all_autoplay_marks.lstrip(self.p1_mark)

        self.setup_game_board()
        self.unbind_game_board()

    def auto_turn_limit(self) -> None:
        """
        Provide for 1000 alternating pc player marks in autoplay turns;
        Good for about 120 games.

        :return: None
        """
        # String of player marks is shortened one character per turn played and
        #  when an autoplay option is set to always begin with p1_mark.
        all_x = self.p1_mark * 500
        all_o = self.p2_mark * 500

        self.all_autoplay_marks = ''.join(map(lambda x, o: x + o, all_x, all_o))

    def set_who_autostarts(self) -> None:
        """
        Toggle who_autostarts Button text.
        Text content used for conditions in auto_setup().

        :return: None
        """
        if self.who_autostarts['text'] == 'Player 1 starts':
            self.who_autostarts['text'] = 'Players alternate'
        else:
            self.who_autostarts['text'] = 'Player 1 starts'

    def autoplay_random(self) -> None:
        """
        Automatically play computer vs. computer for 1000 turns
        (~130 games) or until stopped by user. All play positions are
        random. Each turn is played on a timed interval set by the
        self.auto_after time used in the after_id caller, so one turn
        per call.

        :return: None
        """
        self.curr_automode = 'Autoplay random'
        self.auto_turns_remaining.set(len(self.all_autoplay_marks))
        current_turn = self.turn_number()

        if len(self.all_autoplay_marks) > 0:
            mark = self.all_autoplay_marks[0]

            self.pc_plays_random(current_turn, mark)

            if self.turn_number() >= 5:
                self.check_winner(mark)

            # Need to move to next player's mark for next turn.
            self.all_autoplay_marks = self.all_autoplay_marks.lstrip(mark)

            # Need a pause so user can see what plays were made; allows
            #   auto_stop() to break the call cycle.
            self.after_id = app.after(self.auto_after, self.autoplay_random)
        else:
            self.auto_stop('ended')

    def autoplay_strategy(self) -> None:
        """
        Automatically play computer vs. computer for 1000 turns
        (~120 games) or until stopped by user. Each turn is played on a
        timed interval set by the self.auto_after time used in the
        after_id caller, so one turn per call. Game play is at random
        position unless a win or block is available.

        :return: None
        """

        self.curr_automode = 'Autoplay strategy'
        # Tuples of winning list indices for the board_labels board squares.
        winning_combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),  # diagonals
        ]
        random.shuffle(winning_combos)

        self.auto_turns_remaining.set(len(self.all_autoplay_marks))
        current_turn = self.turn_number()

        if len(self.all_autoplay_marks) > 0:
            mark = self.all_autoplay_marks[0]

            while current_turn == self.turn_number():

                # Play for win.
                if current_turn == self.turn_number():
                    for combo in winning_combos:
                        _x, _y, _z = combo
                        x_txt = self.board_labels[_x]['text']
                        y_txt = self.board_labels[_y]['text']
                        z_txt = self.board_labels[_z]['text']

                        if current_turn == self.turn_number():
                            if x_txt == y_txt == self.p1_mark and z_txt == ' ':
                                self.board_labels[_z]['text'] = mark
                                break
                            if y_txt == z_txt == self.p1_mark and x_txt == ' ':
                                self.board_labels[_x]['text'] = mark
                                break
                            if x_txt == z_txt == self.p1_mark and y_txt == ' ':
                                self.board_labels[_y]['text'] = mark
                                break

                # Play to block
                if current_turn == self.turn_number():
                    for combo in winning_combos:
                        _x, _y, _z = combo
                        x_txt = self.board_labels[_x]['text']
                        y_txt = self.board_labels[_y]['text']
                        z_txt = self.board_labels[_z]['text']

                        if x_txt == y_txt == self.p2_mark and z_txt == ' ':
                            self.board_labels[_z]['text'] = mark
                            break
                        if y_txt == z_txt == self.p2_mark and x_txt == ' ':
                            self.board_labels[_x]['text'] = mark
                            break
                        if x_txt == z_txt == self.p2_mark and y_txt == ' ':
                            self.board_labels[_y]['text'] = mark
                            break

                # Play a random square.
                if current_turn == self.turn_number():
                    self.pc_plays_random(current_turn, mark)

            if self.turn_number() >= 5:
                self.check_winner(mark)

            # Need to move to next mark for next turn.
            self.all_autoplay_marks = self.all_autoplay_marks.lstrip(mark)

            # Need a pause so user can see what plays were made and also
            #   allow auto_stop() to break the call cycle.
            self.after_id = app.after(self.auto_after, self.autoplay_strategy)
        else:
            self.auto_stop('ended')

    def auto_flash(self, combo: tuple, mark: str) -> None:
        """
        For each auto_play win, flashes the winning marks. Flashes the
        center square only on a tie (using combo = (4, 4, 4)), then
        calls auto_setup() for the next auto_play() game.

        :param combo: The tuple index values for the winning squares on
                      the board.
        :param mark: The winning player's mark, usually 'X' or 'O'.
        """
        _x, _y, _z = combo

        def winner_show():
            self.board_labels[_x].config(text=mark, bg=self.color['sq_won'])
            self.board_labels[_y].config(text=mark, bg=self.color['sq_won'])
            self.board_labels[_z].config(text=mark, bg=self.color['sq_won'])
            app.update_idletasks()

        def winner_erase():
            self.board_labels[_x].config(text=' ', bg=self.color['sq_not_won'])
            self.board_labels[_y].config(text=' ', bg=self.color['sq_not_won'])
            self.board_labels[_z].config(text=' ', bg=self.color['sq_not_won'])

        app.after(1, winner_show)
        app.after(300, winner_erase)

        # Need to allow idle time for auto_setup to complete given auto_after
        #   time; keeps all_autoplay_marks in correct register.
        app.after_idle(self.auto_setup)


if __name__ == '__main__':

    # ttt_utils.__init__ runs checks on supported platforms and
    #   Python versions; exits if checks fail.

    utils.manage_args()

    print('tty.py now running...')
    app = TicTacToeGUI()
    app.title('TIC TAC TOE')
    app.resizable(False, False)

    img = tk.PhotoImage(file='images/Tic_tac_toe.png')
    app.wm_iconphoto(True, img)

    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\n*** User quit the program ***\n")
    except Exception as unknown:
        print(f'\nAn unexpected error: {unknown}\n')
        sys.exit(1)

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

# Local program imports:
from ttt_utils import const, utils, platform_check as chk
from ttt_utils.const import P1_MARK, P2_MARK, COLOR


class TicTacToeGUI(tk.Tk):
    """
    Display the tkinter GUI playing board and its control buttons.
    Provide multi-mode play action, with scoring.
    Methods: configure_widgets, your_turn_player1, grid_widgets,
        setup_game_board, unbind_game_board, on_enter, on_leave,
        mode_control, human_turn, pc_turn, play_random, turn_number,
        check_winner, flash_win, flash_tie, window_geometry, display_result,
        block_all_player_action, new_game, reset_game_and_score,
        auto_command, auto_start, auto_stop, auto_setup, auto_turns_limit,
        autoplay_random, autoengine, autoplay_strategy, autoplay_center,
        auto_flash_win.
    """
    # Using __slots__ for Class attributes gives slight reduction of memory
    #   usage and possible performance improvement.
    __slots__ = (
        'after_id', 'auto_erase', 'auto_marks',
        'auto_go_stop_radiobtn', 'auto_go_stop_txt',
        'auto_random_mode', 'auto_strategy_mode', 'auto_center_mode',
        'auto_turns_header', 'auto_turns_lbl', 'auto_turns_remaining',
        'autoplay_on', 'autospeed_fast', 'autospeed_lbl',
        'autospeed_selection', 'autospeed_slow', 'board_labels',
        'choose_pc_pref', 'curr_pmode', 'display_automode', 'font',
        'mode_selection',
        'p1_points', 'p1_score', 'p2_points', 'p2_score',
        'player1_header', 'player1_score_lbl',
        'player2_header', 'player2_score_lbl',
        'prev_game_num', 'prev_game_num_header', 'prev_game_num_lbl',
        'pvp_mode', 'pvpc_mode', 'quit_button', 'result_calls',
        'resultwin_geometry', 'result_window_open', 'score_header',
        'separator', 'ties_header', 'ties_lbl', 'ties_num',
        'titlebar_offset', 'who_autostarts', 'whose_turn',
        'whose_turn_lbl', 'winner_found',
    )

    def __init__(self):
        super().__init__()

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
        self.ties_num = tk.IntVar()
        self.ties_lbl = tk.Label()

        # Play action widgets.
        self.board_labels = [tk.Label() for _ in range(9)]
        self.mode_selection = tk.StringVar()
        self.pvp_mode = tk.Radiobutton()
        self.pvpc_mode = tk.Radiobutton()
        self.choose_pc_pref = ttk.Combobox()
        self.auto_random_mode = tk.Radiobutton()
        self.auto_strategy_mode = tk.Radiobutton()
        self.auto_center_mode = tk.Radiobutton()
        self.autoplay_on = tk.BooleanVar()
        self.auto_go_stop_radiobtn = tk.Radiobutton()
        self.auto_go_stop_txt = tk.StringVar()
        self.who_autostarts = ttk.Button()
        self.autospeed_lbl = tk.Label()
        self.autospeed_selection = tk.StringVar()
        self.autospeed_fast = tk.Radiobutton()
        self.autospeed_slow = tk.Radiobutton()
        self.auto_erase = 0

        self.quit_button = ttk.Button()

        # Additional widgets.
        self.separator = ttk.Separator()
        self.after_id = None  # A handler for after() and after_cancel() calls.
        self.auto_marks = ''  # Used to dole out autoplay marks in proper register.
        self.display_automode = ''  # Used to display whose_turn.
        self.curr_pmode = ''  # Used to evaluate mode state.
        self.result_calls = 0  # Allows recording of initial Result window position.
        self.resultwin_geometry = ''  # Used to remember Result window position.
        self.result_window_open = False  # A flag to prevent duplicate windows.
        self.titlebar_offset = 0  # Used for accurate positioning of Result win.

        self.font = {}  # Dictionary is filled in configure_widgets().

        self.configure_widgets()
        self.grid_widgets()

    def configure_widgets(self) -> None:
        """Initial configurations of app window widgets."""
        ttk.Style().theme_use('alt')

        self.ties_num.set(0)

        self.font = {
            'sm_button': ('TkHeadingFont', 8),
            'who': ('TkHeadingFont', 7, 'italic bold'),
            'button': ('TkHeadingFont', 8, 'bold'),
            'scores': ('TkHeadingFont', 9),
            'report': ('TkHeadingFont', 9, 'italic bold'),
            'condensed': ('TkTooltipFont', 8),
            'mark': ('TkFixedFont', 50),
        }

        # Need to apply OS-specific font adjustments.
        if chk.MY_OS == 'lin':
            self.font['report'] = ('TkHeadingFont', 10, 'italic bold')
        elif chk.MY_OS == 'dar':
            self.font['sm_button'] = ('TkHeadingFont', 10)
            self.font['who'] = ('TkHeadingFont', 11, 'italic bold')
            self.font['button'] = ('TkHeadingFont', 11, 'bold')
            self.font['scores'] = ('TkHeadingFont', 12)
            self.font['report'] = ('TkHeadingFont', 13, 'italic bold')
            self.font['condensed'] = ('TkTooltipFont', 10)

        # Need tk to match system's default white shade.
        if chk.MY_OS == 'dar':
            COLOR['tk_white'] = 'white'
        elif chk.MY_OS == 'lin':
            COLOR['tk_white'] = 'grey85'
        else:  # platform is 'win'
            COLOR['tk_white'] = 'grey95'

        # Player's turn widgets.
        self.prev_game_num_header.config(text='Games played',
                                         font=self.font['condensed'])
        self.prev_game_num_lbl.config(textvariable=self.prev_game_num,
                                      font=self.font['condensed'])
        self.whose_turn_lbl.config(textvariable=self.whose_turn, height=4,
                                   font=self.font['who'])

        self.your_turn_player1()  # Starting prompt for Player1 to begin play.

        self.auto_turns_header.config(text='Turns to go',
                                      font=self.font['condensed'])
        self.auto_turns_lbl.config(textvariable=self.auto_turns_remaining,
                                   font=self.font['condensed'])

        # Players' scores widgets:
        # ︴squiggle symbol from https://coolsymbol.com/line-symbols.html
        self.score_header.config(
            text='Score ︴', font=self.font['scores'],
            fg=COLOR['score_fg'])
        self.player1_header.config(
            text='Player 1:', font=self.font['scores'],
            fg=COLOR['score_fg'])
        self.player2_header.config(
            text='Player 2:', font=self.font['scores'],
            fg=COLOR['score_fg'])
        self.player1_score_lbl.config(
            textvariable=self.p1_score, font=self.font['scores'],
            fg=COLOR['score_fg'])
        self.player2_score_lbl.config(
            textvariable=self.p2_score, font=self.font['scores'],
            fg=COLOR['score_fg'])
        self.ties_header.config(
            text='Ties:', font=self.font['scores'],
            fg=COLOR['score_fg'])
        self.ties_lbl.config(
            textvariable=self.ties_num, font=self.font['scores'],
            fg=COLOR['score_fg'])

        # Play mode control widgets:
        self.pvp_mode.config(text='Player v Player',
                             font=self.font['condensed'],
                             variable=self.mode_selection,
                             value='pvp',
                             command=self.mode_control)
        self.pvp_mode.select()  # Start default mode is Player v Player.

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
                                           # 'PC plays corners',
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
        self.auto_strategy_mode.config(text='Autoplay strategy\n(random 1st)',
                                       font=self.font['condensed'],
                                       variable=self.mode_selection,
                                       value='auto-strategy',
                                       command=self.mode_control)
        self.auto_center_mode.config(text='Autoplay center\n(center 1st)',
                                     font=self.font['condensed'],
                                     variable=self.mode_selection,
                                     value='auto-center',
                                     command=self.mode_control)
        self.auto_go_stop_radiobtn.config(textvariable=self.auto_go_stop_txt,
                                          font=self.font['button'],
                                          variable=self.autoplay_on,
                                          fg=COLOR['mark_fg'],
                                          bg=COLOR['radiobtn_bg'],
                                          borderwidth=2,
                                          indicatoron=False,
                                          command=self.auto_command)
        self.autospeed_lbl.config(text='Auto-speed',
                                  font=self.font['condensed'])
        self.autospeed_fast.config(text='Fast',
                                   font=self.font['condensed'],
                                   variable=self.autospeed_selection,
                                   value='fast',
                                   command=self.autospeed_control)
        self.autospeed_slow.config(text='Slow',
                                   font=self.font['condensed'],
                                   variable=self.autospeed_selection,
                                   value='slow',
                                   command=self.autospeed_control)
        self.autospeed_slow.select()  # Set starting/default auto-speed.

        self.auto_go_stop_txt.set('Start auto')
        self.auto_go_stop_radiobtn.config(state=tk.DISABLED)

        # ttk.Buttons are used b/c tk.Buttons cannot be configured in macOS.
        style = ttk.Style()
        style.map('My.TButton',
                  foreground=[('pressed', COLOR['disabled_fg']),
                              ('active', COLOR['mark_fg']),
                              ('disabled', COLOR['disabled_fg'])
                              ],
                  background=[('pressed', COLOR['tk_white']),
                              ('active', COLOR['radiobtn_bg'])],
                  )
        style.configure('My.TButton', font=self.font['sm_button'])
        self.who_autostarts.configure(style="My.TButton",
                                      text='Player 1 starts', width=14,
                                      state=tk.DISABLED,
                                      takefocus=False,
                                      command=self.autostart_set_who)

        self.quit_button.config(style="My.TButton",
                                text='Quit', width=4,
                                command=lambda: utils.quit_game(mainloop=app))

        # Configure game board playing squares (Labels):
        self.setup_game_board()

    def grid_widgets(self) -> None:
        """Position app window widgets."""

        # Position play action Labels in 3 x 3 grid. Note that while
        #   nothing is gridded in row index 1, the top row uses rowspan=2
        #   to center widgets vertically; hence, board_labels begin on
        #   row index 2.
        _row = 2
        _col = 0

        # Set platform-specific padding between play Labels (squares).
        if chk.MY_OS == 'dar':  # macOS
            pad = 6
        elif chk.MY_OS == 'lin':  # Linux
            pad = 0
        else:  # Windows
            pad = 8

        for lbl in self.board_labels:
            lbl.grid(row=_row, column=_col, pady=pad, padx=pad, ipady=6, ipadx=10)
            _col += 1
            if _col > 2:
                _row += 1
                _col = 0

        # Squeeze everything in with pretty spanning, padding, and stickies.
        #  Grid statements are sorted by row, then column.
        self.whose_turn_lbl.grid(  # padx matches that of board_labels.
            row=0, column=0, padx=0, pady=(5, 0))

        if chk.MY_OS in 'lin, dar':
            self.prev_game_num_header.grid(
                row=0, column=2, rowspan=2, padx=(0, 8), pady=(8, 0), sticky=tk.NE)
            self.prev_game_num_lbl.grid(
                row=0, column=2, rowspan=2, padx=(0, 8), pady=(22, 0), sticky=tk.NE)
        else:  # is Windows
            self.prev_game_num_header.grid(
                row=0, column=2, rowspan=2, padx=(0, 8), pady=(13, 0), sticky=tk.NE)
            self.prev_game_num_lbl.grid(
                row=0, column=2, rowspan=2, padx=(0, 8), pady=(35, 0), sticky=tk.NE)

        # There is duplication in the elif statements to allow easy editing and
        #   cut/paste actions for platform-specific adjustments.
        if chk.MY_OS == 'dar':
            self.score_header.grid(
                row=0, column=1, rowspan=2, padx=(10, 0), pady=(0, 10), sticky=tk.W)
            self.player1_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 0), pady=(0, 35), sticky=tk.E)
            self.player2_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 0), pady=(20, 10), sticky=tk.E)
        elif chk.MY_OS == 'lin':
            self.score_header.grid(
                row=0, column=1, rowspan=2, padx=(10, 0), pady=(0, 10), sticky=tk.W)
            self.player1_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(0, 35), sticky=tk.E)
            self.player2_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(20, 10), sticky=tk.E)
        else:  # is Windows
            self.score_header.grid(
                row=0, column=1, rowspan=2, padx=(10, 0), pady=(0, 10), sticky=tk.W)
            self.player1_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(0, 45), sticky=tk.E)
            self.player2_header.grid(
                row=0, column=1, rowspan=2, padx=(0, 8), pady=(30, 10), sticky=tk.E)

        if chk.MY_OS in 'lin, dar':
            self.player1_score_lbl.grid(
                row=0, column=1,
                rowspan=2, columnspan=2,
                padx=(112, 0), pady=(0, 35), sticky=tk.W)
            self.player2_score_lbl.grid(
                row=0, column=1,
                rowspan=2, columnspan=2,
                padx=(112, 0), pady=(20, 10), sticky=tk.W)
        else:  # is Windows
            self.player1_score_lbl.grid(
                row=0, column=2,
                rowspan=2,
                padx=0, pady=(0, 50), sticky=tk.W)
            self.player2_score_lbl.grid(
                row=0, column=2,
                rowspan=2,
                padx=0, pady=(30, 10), sticky=tk.W)

        # Auto-turn counting labels are gridded in auto_start().

        if chk.MY_OS in 'lin, dar':
            self.ties_header.grid(
                row=0, column=1,
                rowspan=2,
                padx=(0, 8), pady=(55, 0), sticky=tk.E)
            self.ties_lbl.grid(
                row=0, column=1,
                rowspan=2, columnspan=2,
                padx=(112, 0), pady=(55, 0), sticky=tk.W)
        else:  # is Windows
            self.ties_header.grid(
                row=0, column=1,
                rowspan=2,
                padx=(0, 8), pady=(85, 0), sticky=tk.E)
            self.ties_lbl.grid(
                row=0, column=2,
                rowspan=2,
                padx=0, pady=(85, 0), sticky=tk.W)

        if chk.MY_OS == 'dar':
            self.pvp_mode.grid(
                row=5, column=0, padx=(20, 0), pady=5, sticky=tk.W)
            self.pvpc_mode.grid(
                row=5, column=1, columnspan=2, padx=(20, 0), pady=5, sticky=tk.W)
            self.choose_pc_pref.grid(
                row=5, column=1, columnspan=2, padx=(0, 25), pady=0, sticky=tk.E)
        elif chk.MY_OS == 'lin':
            self.pvp_mode.grid(
                row=5, column=0, padx=(10, 0), pady=5, sticky=tk.W)
            self.pvpc_mode.grid(
                row=5, column=1, columnspan=2, padx=(0, 0), pady=5, sticky=tk.W)
            self.choose_pc_pref.grid(
                row=5, column=1, columnspan=2, padx=(0, 35), pady=0, sticky=tk.E)
        else:  # is Windows
            self.pvp_mode.grid(
                row=5, column=0, padx=(25, 0), pady=5, sticky=tk.W)
            self.pvpc_mode.grid(
                row=5, column=1, columnspan=2, padx=(30, 0), pady=5, sticky=tk.W)
            self.choose_pc_pref.grid(
                row=5, column=1, columnspan=2, padx=(0, 45), pady=0, sticky=tk.E)

        self.separator.grid(
            row=7, column=0, columnspan=3, padx=10, sticky=tk.EW)

        self.auto_go_stop_radiobtn.grid(
            row=8, column=1, rowspan=2, padx=8, pady=(6, 0), sticky=tk.W)
        self.autospeed_lbl.grid(
            row=8, column=1,
            rowspan=2, columnspan=2,
            padx=(0, 60), pady=(6, 0),
            sticky=tk.E)
        self.autospeed_fast.grid(
            row=9, column=1,
            columnspan=2,
            padx=(0, 100), pady=(16, 0),
            sticky=tk.E)
        self.autospeed_slow.grid(
            row=9, column=1,
            columnspan=2,
            padx=(0, 40), pady=(16, 0),
            sticky=tk.E)

        if chk.MY_OS in 'win, dar':
            padx = (5, 0)
        else:
            padx = 0
        self.auto_random_mode.grid(
            row=8, column=0, padx=padx, pady=(4, 0), sticky=tk.W)
        self.auto_strategy_mode.grid(
            row=9, column=0, padx=padx, pady=0, sticky=tk.W)
        self.auto_center_mode.grid(
            row=10, column=0, padx=padx, pady=0, sticky=tk.W)

        self.who_autostarts.grid(
            row=11, column=0, padx=(10, 0), pady=5, sticky=tk.W)
        self.quit_button.grid(
            row=11, column=2, padx=5, pady=(0, 5), sticky=tk.E)

    def setup_game_board(self) -> None:
        """
        Configure and activate play action for the game board squares.

        :return: None
        """
        for i, lbl in enumerate(self.board_labels):
            lbl.config(text=' ', height=1, width=2,
                       bg=COLOR['sq_not_won'],
                       fg=COLOR['mark_fg'],
                       font=self.font['mark'],
                       )

            if chk.MY_OS == 'dar':
                lbl.config(borderwidth=12)
            else:  # is Linux or Windows.
                lbl.config(highlightthickness=6)

            lbl.bind('<Button-1>',
                     lambda event, lbl_idx=i:
                     self.human_turn(self.board_labels[lbl_idx])
                     )
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

    @staticmethod
    def on_enter(label: tk) -> None:
        """
        On mouseover, indicate game board square with a COLOR change.

        :param label: The tk.Label object.
        :return: None
       """
        if label['bg'] == COLOR['sq_not_won']:
            label['bg'] = COLOR['sq_mouseover']
        elif label['bg'] == COLOR['sq_won']:
            label['bg'] = COLOR['sq_won']

    @staticmethod
    def on_leave(label: tk):
        """
        On mouse leave, game board square returns to entered COLOR.

        :param label: The tk.Label object.
        :return: None
        """
        if label['bg'] == COLOR['sq_mouseover']:
            label['bg'] = COLOR['sq_not_won']
        elif label['bg'] == COLOR['sq_not_won']:
            label['bg'] = COLOR['sq_not_won']
        elif label['bg'] == COLOR['sq_won']:
            label['bg'] = COLOR['sq_won']

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
                elif mode == 'auto-center':
                    self.auto_center_mode.deselect()
                elif mode == 'pvp':
                    self.pvp_mode.deselect()
                elif mode == 'pvpc':
                    self.pvpc_mode.deselect()

                detail = ('Wait for autoplay to finish,\n'
                          'or click "Stop auto" button.')
                self.whose_turn.set(self.display_automode)

            else:
                if self.curr_pmode == 'pvp':
                    self.pvp_mode.select()
                    self.choose_pc_pref.config(state=tk.DISABLED)
                    self.pvpc_mode.deselect()
                    self.auto_random_mode.deselect()
                    self.auto_strategy_mode.deselect()
                    self.auto_center_mode.deselect()
                elif self.curr_pmode == 'pvpc':
                    self.pvpc_mode.select()
                    self.choose_pc_pref.config(state='readonly')
                    self.pvp_mode.deselect()
                    self.auto_random_mode.deselect()
                    self.auto_strategy_mode.deselect()
                    self.auto_center_mode.deselect()

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
                self.your_turn_player1()
            else:  # One of the auto modes.
                self.auto_go_stop_radiobtn.config(state=tk.NORMAL)
                self.who_autostarts.configure(state=tk.NORMAL)
                self.whose_turn.set('PC autoplay')
                self.whose_turn_lbl.config(bg=COLOR['tk_white'])

            # Need this to deactivate the auto_go_stop_radiobtn which
            #   would otherwise open a duplicate Result window (a
            #   'started' auto game would be instantly 'canceled' b/c the
            #   game board wasn't reset). So force user to click
            #   'New Game' or 'Quit' in Result window BEFORE selecting an
            #   autoplay mode and clicking on an active auto_go_stop_radiobtn.
            if self.result_window_open:
                self.auto_go_stop_radiobtn.config(state=tk.DISABLED)

    def your_turn_player1(self) -> None:
        """
        Display when it is Player 1's turn to play.

        :return: None
        """
        # Need to inform player when it's their turn after PC has played.
        if self.mode_selection.get() == 'pvpc' and self.turn_number() == 1:
            self.whose_turn.set(f'PC played {P2_MARK}\n'
                                f'Your turn {const.PLAYER1}')
        else:
            self.whose_turn.set(f'{const.PLAYER1} plays {P1_MARK}')

        self.whose_turn_lbl.config(bg=COLOR['result_bg'])

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
            played_lbl['text'] = P1_MARK
            self.whose_turn.set(f'{const.PLAYER2} plays {P2_MARK}')
            self.whose_turn_lbl.config(bg=COLOR['tk_white'])

        def h_plays_p2():
            played_lbl['text'] = P2_MARK
            played_lbl.config(fg=COLOR['tk_white'])
            self.your_turn_player1()

        def h_plays_p1_v_pc():
            played_lbl['text'] = P1_MARK
            self.whose_turn_lbl.config(bg=COLOR['tk_white'])
            self.whose_turn.set(f'PC plays {P2_MARK}')

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
                    self.check_winner(P1_MARK)

                if self.turn_number() < 9 and not self.winner_found:
                    self.pc_turn()
        else:
            messagebox.showerror('Oops!', 'This square was already played!')

        self.quit_button.config(command=lambda: utils.quit_game(app, False))

    def color_the_mark(self, _id: int) -> None:
        """
        In PvP and PvPC modes (or any non-auto mode), provide alternate
        colors for Player1 and Player2 marks. Default COLOR
        (COLOR['mark_fg']) is set in setup_game_board().
        This method changes that to an alternate fg.

        :param _id: The board label's list index of the played square.
        :return: None
        """

        if not self.display_automode:
            self.board_labels[_id].config(fg=COLOR['tk_white'])

    def pc_turn(self) -> None:
        """
        Computer plays as Player2 (P2_MARK).
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
            app.after(const.PLAY_AFTER)

        # Need to reorder winner and corner lists so Human doesn't detect a pattern
        #   of where PC will play.
        random.shuffle(const.WINING_COMBOS)
        random.shuffle(const.CORNERS)

        # Loops break with the first p2_mark played.
        while turn_number == self.turn_number():

            # Preference: all PC moves are random.
            if self.choose_pc_pref.get() == 'PC plays random':
                self.play_random(turn_number, P2_MARK)

            # Preference: play the center when it is available.
            elif self.choose_pc_pref.get() == 'PC plays center':
                if self.board_labels[4]['text'] == ' ':
                    self.board_labels[4]['text'] = P2_MARK
                    self.color_the_mark(4)
            # Preference: strategy, adaptive defense to human's first two turns.
            elif self.choose_pc_pref.get() == 'PC plays strategy':
                self.pc_defense(turn_number)

            # Prefer now to play for win, then for block, then what's available.
            # Play to win:
            if turn_number == self.turn_number():
                for combo in const.WINING_COMBOS:
                    _x, _y, _z = combo
                    x_txt = self.board_labels[_x]['text']
                    y_txt = self.board_labels[_y]['text']
                    z_txt = self.board_labels[_z]['text']

                    if x_txt == y_txt == P2_MARK and z_txt == ' ':
                        self.board_labels[_z]['text'] = P2_MARK
                        self.color_the_mark(_z)
                        break
                    if y_txt == z_txt == P2_MARK and x_txt == ' ':
                        self.board_labels[_x]['text'] = P2_MARK
                        self.color_the_mark(_x)
                        break
                    if x_txt == z_txt == P2_MARK and y_txt == ' ':
                        self.board_labels[_y]['text'] = P2_MARK
                        self.color_the_mark(_y)
                        break

            # Play to block:
            #  Note: Need this separate 'if', not elif or continuation of
            #  preceding 'if', to prioritize winning over blocking.
            if turn_number == self.turn_number():
                for combo in const.WINING_COMBOS:
                    _x, _y, _z = combo
                    x_txt = self.board_labels[_x]['text']
                    y_txt = self.board_labels[_y]['text']
                    z_txt = self.board_labels[_z]['text']

                    if x_txt == y_txt == P1_MARK and z_txt == ' ':
                        self.board_labels[_z]['text'] = P2_MARK
                        self.color_the_mark(_z)
                        break
                    if y_txt == z_txt == P1_MARK and x_txt == ' ':
                        self.board_labels[_x]['text'] = P2_MARK
                        self.color_the_mark(_x)
                        break
                    if x_txt == z_txt == P1_MARK and y_txt == ' ':
                        self.board_labels[_y]['text'] = P2_MARK
                        self.color_the_mark(_y)
                        break

                # Strategy defense and obvious moves are taken care of,
                #   so try a corner strategy to win.
                if self.choose_pc_pref.get() == 'PC plays strategy':
                    for _c in const.CORNERS:
                        c_txt = self.board_labels[_c]['text']
                        if turn_number == self.turn_number() and c_txt == ' ':
                            self.board_labels[_c]['text'] = P2_MARK
                            self.color_the_mark(_c)
                            break

            # If no preferred play available, then play random.
            if turn_number == self.turn_number():
                self.play_random(turn_number, P2_MARK)

        if self.turn_number() >= 5:
            self.check_winner(P2_MARK)

        self.your_turn_player1()

        app.update_idletasks()

    def play_random(self, turn_number: int, mark: str) -> None:
        """ Play *mark* in a random position of board_labels index.

        :param mark: The player's mark string to play.
        :param turn_number: The current turn number, from turn_number().

        :return: None
        """
        while turn_number == self.turn_number():
            random_idx = random.randrange(0, 9)
            if self.board_labels[random_idx]['text'] == ' ':
                self.board_labels[random_idx]['text'] = mark
                self.color_the_mark(random_idx)

    def pc_defense(self, turn_number: int) -> None:
        """
        A defensive response to human's first two turns in PvPC mode.
        Purpose is to minimize PC losses.

        :param turn_number: The current turn number, from turn_number().
        :return: None
        """
        # When human starts with a side square, need to play center to
        #   avoid possibility of a loss.
        if turn_number in (1, 5):
            for _s in const.SIDES:
                s_txt = self.board_labels[_s]['text']
                if s_txt == P1_MARK:
                    if self.board_labels[4]['text'] == ' ':
                        self.board_labels[4]['text'] = P2_MARK
                        self.color_the_mark(4)
                        break
        # When human is on two adjacent side squares, need to defend with
        #   PC play to the common corner to avoid possibility of a loss.
        if turn_number == 3:
            side_list = []
            for _s in const.SIDES:
                s_txt = self.board_labels[_s]['text']
                if s_txt == P1_MARK:
                    side_list.append(_s)

            if side_list == [1, 3] and self.board_labels[0]['text'] == ' ':
                self.board_labels[0]['text'] = P2_MARK
                self.color_the_mark(0)
            elif side_list == [1, 5] and self.board_labels[2]['text'] == ' ':
                self.board_labels[2]['text'] = P2_MARK
                self.color_the_mark(2)
            elif side_list == [3, 7] and self.board_labels[6]['text'] == ' ':
                self.board_labels[6]['text'] = P2_MARK
                self.color_the_mark(6)
            elif side_list == [5, 7] and self.board_labels[8]['text'] == ' ':
                self.board_labels[8]['text'] = P2_MARK
                self.color_the_mark(8)

    def turn_number(self) -> int:
        """
        Keep count of turns per game by counting play labels with
        label text other than a space string.

        :return: The number of turns played, as integer.
        """
        return len([i for i in self.board_labels if ' ' not in i['text']])

    def check_winner(self, mark: str) -> None:
        """
        Check each player's played *mark* (board_labels's text value)
        and evaluate whether played marks match a positional win in the
        board matrix (based on board_labels index values).

        :param mark: The played mark character to check for a win.
        :return: None
        """

        def award_points(winning_mark):
            if winning_mark == P1_MARK:
                self.p1_points += 1
            else:
                self.p2_points += 1

        # Loop breaks when the first winning combo is found.
        for combo in const.WINING_COMBOS:
            _x, _y, _z = combo
            lbl_x_txt = self.board_labels[_x]['text']
            lbl_y_txt = self.board_labels[_y]['text']
            lbl_z_txt = self.board_labels[_z]['text']

            if lbl_x_txt == lbl_y_txt == lbl_z_txt == mark:
                self.winner_found = True
                self.prev_game_num.set(self.prev_game_num.get() + 1)

                # Record to file all winning board_labels lists.
                # winlist = f'{[i["text"] for i in self.board_labels]}\n'
                # with open('wins', 'a') as file:
                #     file.write(winlist)

                if 'auto-' in self.mode_selection.get():
                    award_points(mark)
                    self.auto_flash_win(combo, mark)
                    break

                # Not an auto- mode, so mode selection is pvp or pvpc.
                award_points(mark)
                self.flash_win(combo)
                self.display_result(f'{mark} WINS!')
                break

        if self.turn_number() == 9 and not self.winner_found:
            self.winner_found = True
            self.prev_game_num.set(self.prev_game_num.get() + 1)

            # Record to file all tied board_labels lists.
            # tielist = f'{[i["text"] for i in self.board_labels]}\n'
            # with open('ties', 'a') as file:
            #     file.write(tielist)

            self.p1_points += 0.5
            self.p2_points += 0.5

            self.ties_num.set(self.ties_num.get() + 1)

            if 'auto-' in self.mode_selection.get():
                self.auto_flash_win((4, 4, 4), 'TIE')
            else:
                self.flash_tie()
                self.display_result('IT IS A TIE!')

    def flash_win(self, combo) -> None:
        """
        Flashes the three winning squares, in series.
        Based on Bryan Oakley's answer for
        how-to-make-a-button-flash-using-after-in-tkinter
        https://stackoverflow.com/a/57298778

        :return: None
        """
        _x, _y, _z = combo

        app.after(10, lambda: self.board_labels[_x].config(bg=COLOR['sq_won']))
        app.after(200, lambda: self.board_labels[_y].config(bg=COLOR['sq_won']))
        app.after(400, lambda: self.board_labels[_z].config(bg=COLOR['sq_won']))

    def flash_tie(self) -> None:
        """
        Make entire game board blue (COLOR['sq_won']) on a tie game.

        :return: None
        """
        for lbl in self.board_labels:
            lbl.config(bg=COLOR['sq_won'])
            app.update_idletasks()

    def window_geometry(self, toplevel: tk) -> None:
        """
        Set the xy geometry of a *toplevel* window near top-left corner
        of app window. If it is moved, then put at the new geometry
        determined by the resultwin_geometry variable.
        Calculate the height of the system's window title bar to use as
        a y-offset for the *toplevel* xy geometry.

        :param toplevel: The tkinter toplevel object to position.
        :return: None
        """

        if self.resultwin_geometry:
            toplevel.geometry(self.resultwin_geometry)
        else:
            toplevel.geometry(f'+{app.winfo_x()}+{app.winfo_y()}')

        # Need to position the geometry of the Report window by applying
        #   a y offset for the height of the system's window title bar.
        #   This is needed because tkinter widget geometry does not
        #   include the system's title bar.
        # Title bar height is determined only once from the initial
        #   placement of the Report window at top-left of the app window.
        if self.result_calls == 1:
            app.update_idletasks()
            self.titlebar_offset = toplevel.winfo_y() - app.winfo_y()

    def display_result(self, result_msg: str) -> None:
        """
        Pop-up a game result window to announce winner or tie with
        PvP and PvPC modes, or with a canceled autoplay.
        Provide option Buttons to play again or quit app.
        Play again option can be invoked with Return or Enter.
        Display tally of players' wins within a single play mode.

        :param result_msg: The result string to display in result window.
        :return: None
        """
        self.result_window_open = True

        result_window = tk.Toplevel(self, borderwidth=4, relief='raised')
        result_window.title('Result')
        result_window.config(bg=COLOR['result_bg'])

        if chk.MY_OS == 'win':  # Windows
            geom = '420x150'
            minw = 270
            minh = 150
        elif chk.MY_OS == 'dar':  # macOS
            geom = '190x90'
            minw = 140
            minh = 90
        else:  # Linux
            geom = '230x100'
            minw = 180
            minh = 100

        result_window.geometry(geom)
        result_window.minsize(minw, minh)

        self.result_calls += 1
        self.window_geometry(result_window)

        # Need prevent focus shifting to app window which would cover up
        #  the Report window.
        result_window.attributes('-topmost', True)
        result_window.focus_force()

        result_lbl = tk.Label(result_window, text=result_msg,
                              font=self.font['report'],
                              bg=COLOR['result_bg'])

        self.block_all_player_action()
        self.whose_turn.set('Game pending...')
        self.whose_turn_lbl.config(bg=COLOR['tk_white'])

        # Need to update players' cumulative wins in the app window.
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        def no_exit_on_x():
            messagebox.showinfo(
                parent=result_window,
                title='Click a button',
                detail='Use either "New Game" or "Quit"'
                       ' to close Report window.')

        result_window.protocol('WM_DELETE_WINDOW', no_exit_on_x)

        def restart_game():
            """
            Record current xy geometry of Report window, reset game
            board, then close window. Called from keybind and Button cmd.

            :return: None
            """

            # Need to retain screen position of results window between games in case
            #   user has moved it from default position.
            self.resultwin_geometry = (
                f'+{result_window.winfo_x()}'
                f'+{result_window.winfo_y() - self.titlebar_offset}'
            )
            self.new_game()
            self.result_window_open = False
            result_window.destroy()

        again = tk.Button(result_window, text='New Game (\u23CE)',
                          # Unicode Return/Enter key symbol.
                          font=self.font['button'],
                          relief='groove', overrelief='raised', border=3,
                          command=restart_game)
        not_again = tk.Button(result_window, text='Quit',
                              font=self.font['sm_button'],
                              relief='groove', overrelief='raised', border=3,
                              command=lambda: utils.quit_game(mainloop=app))
        result_window.bind('<Return>', lambda _: restart_game())
        result_window.bind('<KP_Enter>', lambda _: restart_game())

        result_lbl.pack(pady=3, padx=3)
        again.pack(pady=(0, 0))
        not_again.pack(pady=5)

    def block_all_player_action(self) -> None:
        """
        Prevent user action in app window while Game Report window is
        open. Called from display_result().

        :return: None
        """
        self.unbind_game_board()
        self.quit_button.config(state=tk.DISABLED)
        self.auto_go_stop_radiobtn.config(state=tk.DISABLED)

    def new_game(self) -> None:
        """
        Set up the next game. Called from display_result().

        return: None
        """
        self.quit_button.config(state=tk.NORMAL,
                                command=lambda: utils.quit_game(mainloop=app))
        if 'auto-' in self.mode_selection.get():
            self.auto_go_stop_txt.set('Start auto')
            self.auto_go_stop_radiobtn.config(state=tk.NORMAL)

        self.auto_turns_header.grid_remove()
        self.auto_turns_lbl.grid_remove()

        self.setup_game_board()
        self.winner_found = False

        if self.mode_selection.get() == 'pvp':
            if self.prev_game_num.get() % 2 == 0:
                self.your_turn_player1()
            else:
                self.whose_turn.set(f'{const.PLAYER2} plays {P2_MARK}')
                self.whose_turn_lbl.config(bg=COLOR['tk_white'])

        elif self.mode_selection.get() == 'pvpc':
            if self.prev_game_num.get() % 2 != 0:
                self.whose_turn.set(f'PC plays {P2_MARK}')
                self.whose_turn_lbl.config(bg=COLOR['tk_white'])

                self.pc_turn()
            else:
                self.your_turn_player1()

        # At the end of an autoplay series or when stopped by user, need
        #   to clear auto scores and games.
        if ('Autoplay' in self.display_automode or
                self.auto_turns_remaining.get() > 0):
            self.reset_game_and_score()
            self.display_automode = ''
            self.auto_turns_remaining.set(0)
            self.auto_marks = ''

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
        Toggles text displayed on auto_go_stop_radiobtn.
        Called as the auto_go_stop_radiobtn command.

        :return: None
        """
        if 'Start' in self.auto_go_stop_txt.get():
            if 'auto-' in self.mode_selection.get():
                self.auto_go_stop_txt.set('Stop auto')
                self.autoplay_on.set(True)
                self.auto_start()
            else:
                self.auto_go_stop_txt.set('Start auto')
                self.autoplay_on.set(False)

        else:
            self.auto_go_stop_txt.set('Start auto')
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
        self.whose_turn_lbl.config(bg=COLOR['tk_white'])

        self.auto_turns_lbl.grid(row=0, column=2, rowspan=2,
                                 padx=(0, 8), pady=(0, 0), sticky=tk.SE)
        if chk.MY_OS in 'lin, dar':
            self.auto_turns_header.grid(row=0, column=2, rowspan=2,
                                        padx=(0, 8), pady=(0, 16), sticky=tk.SE)
        else:  # is Windows
            self.auto_turns_header.grid(row=0, column=2, rowspan=2,
                                        padx=(0, 8), pady=(0, 30), sticky=tk.SE)

        self.auto_go_stop_radiobtn.config(state=tk.NORMAL)
        self.who_autostarts.config(state=tk.DISABLED)

        self.auto_turns_limit()
        self.auto_setup()

        # Start repeating calls to one of the autoplay methods;
        #   calls are controlled by after_id.
        if self.mode_selection.get() == 'auto-random':
            self.autoplay_random()
        elif self.mode_selection.get() == 'auto-strategy':
            self.autoplay_strategy()
        elif self.mode_selection.get() == 'auto-center':
            self.autoplay_center()

    def auto_stop(self, stop_msg: str) -> None:
        """
        Stop autoplay method and call Result popup window.
        Disable player game actions (resets when Result window closes).

        :param stop_msg: Information on source of auto_stop call.
        :return: None
        """
        if self.after_id:
            app.after_cancel(self.after_id)
            self.after_id = None

        self.who_autostarts.config(state=tk.NORMAL)

        self.setup_game_board()
        self.display_result(f'{self.display_automode}, {stop_msg}')

    def auto_setup(self) -> None:
        """
        Run at the start of every new autoplay game. Update cumulative
        scores in the app window. Clear all marks from the board.
        Called from auto_start() and auto_flash_win().

        :return: None
        """
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        self.winner_found = False
        if len(self.auto_marks) > 0:
            if self.who_autostarts['text'] == 'Player 1 starts':
                # All games start with p1_mark.
                self.auto_marks = self.auto_marks.lstrip(P2_MARK)
            else:
                # Games alternate starts between p1_mark and p2_mark.
                if self.prev_game_num.get() % 2 == 0:
                    self.auto_marks = self.auto_marks.lstrip(P2_MARK)
                else:
                    self.auto_marks = self.auto_marks.lstrip(P1_MARK)

        self.setup_game_board()
        self.unbind_game_board()

    def auto_turns_limit(self) -> None:
        """
        Provide for 1000 alternating pc player marks in autoplay turns;
        Good for about 120 games.

        :return: None
        """
        # String of player marks is shortened one character per turn played and
        #  when an autoplay option is set to always begin with p1_mark.
        marks1 = P1_MARK * 500
        marks2 = P2_MARK * 500

        self.auto_marks = ''.join(map(lambda m1, m2: m1 + m2, marks1, marks2))

    def autostart_set_who(self) -> None:
        """
        Toggle who_autostarts Button text.
        Text content used for conditions in auto_setup().

        :return: None
        """
        if self.who_autostarts['text'] == 'Player 1 starts':
            self.who_autostarts['text'] = 'Players alternate'
        else:
            self.who_autostarts['text'] = 'Player 1 starts'

    def autospeed_control(self) -> int:
        """
        Set after() times used in auto_flash_win() and autoplay modes.
        Called as Radiobutton command from self.autospeed_fast and
        self.autospeed_slow.
        Called from auto_flash_win() to set time for auto_erase.

        :return: Milliseconds to use in after() calls.
        """

        if self.autospeed_selection.get() == 'fast':
            auto_after = const.AUTO_FAST
        else:
            auto_after = const.AUTO_SLOW

        # Note: Erase time needs to be less than auto_after time for
        #   proper display of game board winner/result flash.
        self.auto_erase = int(auto_after * 0.9)

        return auto_after

    def autoplay_random(self) -> None:
        """
        Automatically play computer vs. computer for 1000 turns
        (~130 games) or until stopped by user. All play positions are
        random. Each turn is played on a timed interval set by the
        utils.PLAY_AFTER time used in the after_id caller, so one turn
        per call.

        :return: None
        """
        self.display_automode = 'Autoplay random'
        self.auto_turns_remaining.set(len(self.auto_marks))
        turn_number = self.turn_number()

        if len(self.auto_marks) > 0:
            mark = self.auto_marks[0]

            self.play_random(turn_number, mark)

            if self.turn_number() >= 5:
                self.check_winner(mark)

            # Need to move to next player's mark for next turn.
            self.auto_marks = self.auto_marks.lstrip(mark)

            # Need a pause so user can see what plays were made; allows
            #   auto_stop() to break the call cycle.
            self.after_id = app.after(self.autospeed_control(),
                                      self.autoplay_random)
        else:
            self.auto_stop('ended')

    def autoengine(self, turn_number: int, mark: str) -> None:
        """
        The rules engine for autoplay option. Prioritizes winning play
        over blocking play over random play.
        Check if able to complete or block a winning combination of
        board labels; play random if neither available.
        Called from autoplay_strategy(), autoplay_center().
        :param turn_number: Current turn count from turn_number().
        :param mark: The played mark character string play.

        :returns: None
        """

        # Play to win.
        if turn_number == self.turn_number():
            for combo in const.WINING_COMBOS:
                _x, _y, _z = combo
                x_txt = self.board_labels[_x]['text']
                y_txt = self.board_labels[_y]['text']
                z_txt = self.board_labels[_z]['text']

                if x_txt == y_txt == P1_MARK and z_txt == ' ':
                    self.board_labels[_z]['text'] = mark
                    break
                if y_txt == z_txt == P1_MARK and x_txt == ' ':
                    self.board_labels[_x]['text'] = mark
                    break
                if x_txt == z_txt == P1_MARK and y_txt == ' ':
                    self.board_labels[_y]['text'] = mark
                    break

        # ...if can't win, then play to block
        if turn_number == self.turn_number():
            for combo in const.WINING_COMBOS:
                _x, _y, _z = combo
                x_txt = self.board_labels[_x]['text']
                y_txt = self.board_labels[_y]['text']
                z_txt = self.board_labels[_z]['text']

                if x_txt == y_txt == P2_MARK and z_txt == ' ':
                    self.board_labels[_z]['text'] = mark
                    break
                if y_txt == z_txt == P2_MARK and x_txt == ' ':
                    self.board_labels[_x]['text'] = mark
                    break
                if x_txt == z_txt == P2_MARK and y_txt == ' ':
                    self.board_labels[_y]['text'] = mark
                    break

        # If no preferred play available, then play random.
        if turn_number == self.turn_number():
            self.play_random(turn_number, mark)

    def autoplay_strategy(self) -> None:
        """
        Automatically play computer vs. computer for 1000 turns
        (~120 games) or until stopped by user. Each turn is played on a
        timed interval set by the self.autospeed_control() time used in the
        after_id caller, so one turn per call. First play is at a
        random position, subsequent plays follow win or block rules.

        :return: None
        """
        self.display_automode = 'Autoplay strategy'

        self.auto_turns_remaining.set(len(self.auto_marks))
        turn_number = self.turn_number()

        if len(self.auto_marks) > 0:
            mark = self.auto_marks[0]

            while turn_number == self.turn_number():
                self.autoengine(turn_number, mark)

            if self.turn_number() >= 5:
                self.check_winner(mark)

            # Need to move to next mark for next turn.
            self.auto_marks = self.auto_marks.lstrip(mark)

            # Need a pause so user can see what plays were made and also
            #   allow auto_stop() to break the call cycle.
            self.after_id = app.after(self.autospeed_control(),
                                      self.autoplay_strategy)
        else:
            self.auto_stop('ended')

    def autoplay_center(self) -> None:
        """
        Automatically play computer vs. computer for 1000 turns
        (~120 games) or until stopped by user. Each turn is played on a
        timed interval set by the autospeed_control() time used in the
        after_id caller, so, one turn per call. First play is at the
        center position, subsequent plays follow win or block rules.

        :return: None
        """
        self.display_automode = 'Autoplay center'

        self.auto_turns_remaining.set(len(self.auto_marks))
        turn_number = self.turn_number()

        if len(self.auto_marks) > 0:
            mark = self.auto_marks[0]

            while turn_number == self.turn_number():
                if self.board_labels[4]['text'] == ' ':
                    self.board_labels[4]['text'] = mark

                self.autoengine(turn_number, mark)

            if self.turn_number() >= 5:
                self.check_winner(mark)

            # Need to move to next mark for next turn.
            self.auto_marks = self.auto_marks.lstrip(mark)

            # Need a pause so user can see what plays were made and also
            #   allow auto_stop() to break the call cycle.
            self.after_id = app.after(self.autospeed_control(),
                                      self.autoplay_center)
        else:
            self.auto_stop('ended')

    def auto_flash_win(self, combo: tuple, mark: str) -> None:
        """
        For each auto_play win, flashes the winning marks. Flashes the
        center square only on a tie (using combo = (4, 4, 4)), then
        calls auto_setup() for the next auto_play() game. Note that on
        a tie, the last played mark does not show on the game board.

        :param combo: The tuple index values for the winning squares on
                      the board.
        :param mark: The winning player's mark, usually 'X' or 'O'.
        """
        _x, _y, _z = combo

        def winner_show():
            self.board_labels[_x].config(text=mark, bg=COLOR['sq_won'])
            self.board_labels[_y].config(text=mark, bg=COLOR['sq_won'])
            self.board_labels[_z].config(text=mark, bg=COLOR['sq_won'])
            app.update_idletasks()

        def winner_erase():
            self.board_labels[_x].config(text=' ', bg=COLOR['sq_not_won'])
            self.board_labels[_y].config(text=' ', bg=COLOR['sq_not_won'])
            self.board_labels[_z].config(text=' ', bg=COLOR['sq_not_won'])

        self.autospeed_control()  # Set auto_erase time.
        app.after(const.AUTO_SHOW, winner_show)
        app.after(self.auto_erase, winner_erase)

        # Need to allow idle time for auto_setup to complete given
        #   autospeed_control() time; keeps auto_marks in correct register.
        app.after_idle(self.auto_setup)


if __name__ == '__main__':

    # ttt_utils.__init__ runs checks on supported platforms and
    #   Python versions; exits if checks fail.

    utils.manage_args()

    print('tty.py now running...')
    # ^^^ If, for some reason, import Path from pathlib is used, then can
    #  print file name as f'{Path(sys.modules["__main__"].__file__).stem}

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

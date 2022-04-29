#!/usr/bin/env python3

"""
Inspired by Riya Tendulkar code:
https://levelup.gitconnected.com/how-to-code-tic-tac-toe-in-python-using-tkinter-e7f9ce510bfb
https://gist.github.com/riya1620/72c2b668ef29da061c44d97a82318572
"""

import random
import sys

# Check for minimum version required:
if sys.version_info < (3, 6):
    print(f'Sorry, but this program requires Python 3.6 or later.\n'
          'Current Python version:'
          f' {sys.version_info.major}.{sys.version_info.minor}\n'
          'Python downloads are available from https://docs.python.org/')
    sys.exit(0)

try:
    import tkinter as tk
    from tkinter import messagebox
except (ImportError, ModuleNotFoundError) as error:
    print(f'This program requires tkinter, which is included with \n'
          'Python 3.7+ distributions.\n'
          'Install the most recent version or re-install Python and include Tk/Tcl.\n'
          '\nOn Linux, you may also need: $ sudo apt-get install python3-tk\n'
          f'See also: https://tkdocs.com/tutorial/install.html \n{error}')

MY_OS = sys.platform[:3]


def quit_game(quit_now=True):
    """
    Manage app window Quit button. Ask for confirmation if a game has
    not yet finished.
    """
    if quit_now:
        print("*** User quit the program ***\n")
        app.destroy()
    else:
        msg = messagebox.askquestion(
            'Confirm', 'Current game is in play.\nQuit now?')
        if msg:
            print("*** User quit the program ***\n")
            app.destroy()


class TicTacToeGUI(tk.Tk):
    """Display the GUI playing board and control buttons."""

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
        self.num_game = 1
        self.winner_found = False

        # Player's turn widgets.
        self.whose_turn = tk.StringVar()
        self.whose_turn_lbl = tk.Label()
        self.auto_turns_header = tk.Label()
        self.auto_turns_lbl = tk.Label()

        # Players' scores widgets.
        self.score_header = tk.Label()
        self.player1_header = tk.Label()
        self.player2_header = tk.Label()
        self.player1_score_lbl = tk.Label()
        self.player2_score_lbl = tk.Label()

        # Play action widgets.
        self.play_labels = [tk.Label() for _ in range(9)]  # The 9 game squares.
        self.mode_selection = tk.StringVar()
        self.pvp_mode = tk.Radiobutton()
        self.pvpc_mode = tk.Radiobutton()
        self.pc_rando_mode = tk.Radiobutton()
        self.pc_compet_mode = tk.Radiobutton()
        self.autoplay_on = tk.BooleanVar()
        self.auto_go_stop_rbtn = tk.Radiobutton()
        self.auto_go_stop = tk.StringVar(value='Start autoplay')
        self.quit_button = tk.Button()

        # Additional autoplay widgets.
        self.after_id = None
        self.play_after = 600  # ms, pause between turns in play PC mode.
        self.auto_after = 250  # ms, pause autoplay turns and game turnovers.
        self.all_autoplay_marks = ''
        self.auto_turns_remaining = tk.IntVar()

        # Foreground and background colors.
        self.color = {'score_fg': 'DodgerBlue4',
                      'result_bg': 'yellow3',
                      'disabled_fg': 'grey65',
                      'active_fg': 'black',
                      'mark_fg': 'yellow2',
                      'sq_won': 'blue',
                      'sq_not_won': 'black',
                      'sq_mouseover': 'grey15',
                      'go-stop_bg': 'DodgerBlue1',
                      }

        # Label fonts.
        self.font = {
            'head11': ('TkHeadingFont', 11, 'italic bold'),
            'head12bold': ('TkHeadingFont', 12, 'bold'),
            'head10bold': ('TkHeaderFont', 10, 'bold'),
            'head10': ('TkHeaderFont', 10),
            'condensed9': ('TkTooltipFont', 9),
            'fixed30bold': ('TkFixedFont', 30, 'bold'),
            'head14boldital': ('TkHeadingFont', 14, 'bold italic'),
        }

        self.configure_widgets()
        self.grid_widgets()

    def configure_widgets(self) -> None:
        """Initial configurations for app window widgets."""
        # Player's turn widgets.
        self.whose_turn_lbl.config(textvariable=self.whose_turn, height=4,
                                   font=self.font['head11'])
        self.whose_turn.set(f'Turn:\n{self.player1} plays {self.p1_mark}')
        self.auto_turns_header.config(text='Turns remaining',
                                      font=self.font['condensed9'])
        self.auto_turns_lbl.config(textvariable=self.auto_turns_remaining,
                                   font=self.font['condensed9'])

        # Players' scores widgets.
        # ︴symbol from https://coolsymbol.com/line-symbols.html
        self.score_header.config(
            text='Score ︴', font=self.font['head12bold'],
            fg=self.color['score_fg'])
        self.player1_header.config(
            text='Player 1:', font=self.font['head10bold'],
            fg=self.color['score_fg'])
        self.player2_header.config(
            text='Player 2:', font=self.font['head10bold'],
            fg=self.color['score_fg'])
        self.player1_score_lbl.config(
            textvariable=self.p1_score, font=self.font['head12bold'],
            fg=self.color['score_fg'])
        self.player2_score_lbl.config(
            textvariable=self.p2_score, font=self.font['head12bold'],
            fg=self.color['score_fg'])

        self.pvp_mode.config(text='Player v Player',
                             variable=self.mode_selection,
                             value='pvp',
                             command=self.block_mode_switch)
        self.pvp_mode.select()
        self.pvpc_mode.config(text='Player v PC',
                              variable=self.mode_selection,
                              value='pvpc',
                              command=self.block_mode_switch)
        self.pc_rando_mode.config(text='Autoplay, random',
                                  variable=self.mode_selection,
                                  value='random',
                                  command=self.block_mode_switch)
        self.pc_compet_mode.config(text='Autoplay, strategy',
                                   variable=self.mode_selection,
                                   value='competitive',
                                   command=self.block_mode_switch)

        self.auto_go_stop_rbtn.config(textvariable=self.auto_go_stop,
                                      variable=self.autoplay_on,
                                      # width=9, # width ignored with sticky EW.
                                      bg=self.color['go-stop_bg'],
                                      font=self.font['head10bold'],
                                      command=self.auto_ctrl,
                                      borderwidth=2,
                                      indicatoron=False,
                                      )

        self.quit_button.config(text='Quit', command=quit_game)

        self.reset_board()

    def grid_widgets(self) -> None:
        """Position app window widgets. Configure play mode buttons."""

        # Position play action buttons in 3 x 3 grid. Note that while
        #   nothing is gridded in row index 1, the top row uses rowspan=2
        #   to center widgets vertically; hence, play buttons begin on
        #   row index 2.
        _row = 2
        _col = 0
        for lbl in self.play_labels:
            if MY_OS in 'win, dar':
                lbl.grid(column=_col, row=_row, pady=6, padx=6)
            else:  # Linux (lin)
                lbl.grid(column=_col, row=_row)
            _col += 1
            if _col > 2:
                _col = 0
                _row += 1

        # Squeeze everything in with pretty spanning, padding, and stickies.
        self.whose_turn_lbl.grid(row=0, column=0, rowspan=2,
                                 padx=(12, 0), sticky=tk.W)

        if MY_OS == 'dar':
            self.score_header.grid(row=0, column=1, rowspan=2,
                                   padx=(50, 0), sticky=tk.W)
        else:
            self.score_header.grid(row=0, column=1, rowspan=2,
                                   padx=(20, 0), sticky=tk.W)

        self.player1_header.grid(row=0, column=1, rowspan=2,
                                 padx=(0, 8), pady=(0, 30), sticky=tk.E)
        self.player2_header.grid(row=0, column=1, rowspan=2,
                                 padx=(0, 8), pady=(30, 0), sticky=tk.E)

        self.player1_score_lbl.grid(row=0, column=2, rowspan=2,
                                    padx=(0, 0), pady=(0, 30), sticky=tk.W)
        self.player2_score_lbl.grid(row=0, column=2, rowspan=2,
                                    padx=(0, 0), pady=(30, 0), sticky=tk.W)
        # Auto-turn counting labels are gridded in auto_start().
        self.pvp_mode.grid(column=0, row=5, padx=(10, 0), pady=(5, 5), sticky=tk.W)
        self.pvpc_mode.grid(column=1, row=5, padx=(10, 0), pady=(5, 5), sticky=tk.W)
        self.pc_rando_mode.grid(column=0, row=7, padx=(10, 0), pady=(8, 0), sticky=tk.W)
        self.pc_compet_mode.grid(column=0, row=8, padx=(10, 0), pady=(0, 0), sticky=tk.W)

        self.auto_go_stop_rbtn.grid(row=7, column=1, rowspan=2,
                                    padx=(0, 0), pady=(0, 10), sticky=tk.EW)

        self.quit_button.grid(row=8, column=2,
                              padx=(0, 10), pady=(5, 8), sticky=tk.E)

    def reset_board(self) -> None:
        """
        Configure and activate play action for the game board squares.
        """
        for i, lbl in enumerate(self.play_labels):
            lbl.config(text=' ', height=3, width=6,
                       bg=self.color['sq_not_won'], fg=self.color['mark_fg'],
                       font=self.font['fixed30bold'],
                       )
            if MY_OS == 'dar':
                lbl.config(borderwidth=12)
            else:
                lbl.config(highlightthickness=6)

            lbl.bind('<Button-1>', lambda event, lbl_idx=i: self.player_turn(
                self.play_labels[lbl_idx]))
            lbl.bind('<Enter>', lambda event, l=lbl: self.on_enter(l))
            lbl.bind('<Leave>', lambda event, l=lbl: self.on_leave(l))

    def on_enter(self, label: tk):
        """
        Indicate mouseover squares with a color change.

        :param label: The tk.Label object.
        """
        if label['bg'] == self.color['sq_not_won']:
            label['bg'] = self.color['sq_mouseover']
        elif label['bg'] == self.color['sq_won']:
            label['bg'] = self.color['sq_won']

    def on_leave(self, label: tk):
        """
        On mouse leave, square returns to entry color.

        :param label: The tk.Label object.
        """
        if label['bg'] == self.color['sq_mouseover']:
            label['bg'] = self.color['sq_not_won']
        elif label['bg'] == self.color['sq_not_won']:
            label['bg'] = self.color['sq_not_won']
        elif label['bg'] == self.color['sq_won']:
            label['bg'] = self.color['sq_won']

    def player_turn(self, played_lbl: tk) -> None:
        """
        Check whether square (*played_lbl*) selected by players is
        available to play.
        Assign player's mark to text value of the selected label.
        In Player v Player, player's alternate who plays first in
        consecutive games and players' marks also alternate.
        In Player v PC mode, Player 1 (human) always has the first turn.
        Evaluate players' turns for a win after 5th turn.

        :param played_lbl: The tk.Label object that was clicked.
        """
        if played_lbl['text'] == ' ':
            if self.mode_selection.get() == 'pvpc':
                if self.turn_number() % 2 == 0:
                    played_lbl['text'] = self.p1_mark
                    self.whose_turn.set(f'Turn:\nCOMPUTER, {self.p2_mark}')

                    # Need update to see the pc_turn() play delayed by app.after.
                    app.update_idletasks()

                    if self.turn_number() < 9 and not self.winner_found:
                        self.pc_turn()

            elif self.mode_selection.get() == 'pvp':
                if self.turn_number() % 2 == 0:
                    played_lbl['text'] = self.p1_mark
                    self.whose_turn.set(f'Turn:\n{self.player2} plays {self.p2_mark}')
                else:
                    played_lbl['text'] = self.p2_mark
                    self.whose_turn.set(f'Turn:\n{self.player1} plays {self.p1_mark}')

            if self.turn_number() >= 5:
                self.check_winner()

        else:
            messagebox.showerror('Oops!', 'This square was already played!')

        self.quit_button.config(command=lambda: quit_game(False))

    def pc_turn(self):
        """
        Computer plays Player2 when called from player_turn().
        Play the center square if open, otherwise block any two Player1
        marks in a row; if none, then randomly play first available square.
        Algorithm favors PC blocking over winning to counter Player1's
        advantage of always playing first.
        """

        # Delay play for a better feel.
        #   With this, need app.update_idletasks() after Player 1 plays.
        app.after(self.play_after)

        # Initial idea for algorithm:
        # https://www.simplifiedpython.net/python-tic-tac-toe-using-artificial-intelligence/
        winning_combos = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),  # diagonals
        )

        pc_turn = self.turn_number()

        while pc_turn == self.turn_number():
            if self.play_labels[4]['text'] == ' ':
                self.play_labels[4]['text'] = self.p2_mark

            else:
                # combo loop is broken when p2_mark is played, adding a turn.
                #  If no play in loop, then play a random open square.
                for combo in winning_combos:
                    _x, _y, _z = combo
                    x_txt = self.play_labels[_x]['text']
                    y_txt = self.play_labels[_y]['text']
                    z_txt = self.play_labels[_z]['text']

                    if pc_turn == self.turn_number():
                        if x_txt == y_txt == self.p1_mark and z_txt == ' ':
                            self.play_labels[_z]['text'] = self.p2_mark
                        elif y_txt == z_txt == self.p1_mark and x_txt == ' ':
                            self.play_labels[_x]['text'] = self.p2_mark
                        elif x_txt == z_txt == self.p1_mark and y_txt == ' ':
                            self.play_labels[_y]['text'] = self.p2_mark
                        elif x_txt == y_txt == self.p2_mark and z_txt == ' ':
                            self.play_labels[_z]['text'] = self.p2_mark
                        elif y_txt == z_txt == self.p2_mark and x_txt == ' ':
                            self.play_labels[_x]['text'] = self.p2_mark
                        elif x_txt == z_txt == self.p2_mark and y_txt == ' ':
                            self.play_labels[_y]['text'] = self.p2_mark

                if pc_turn == self.turn_number():
                    lbl_idx = random.randrange(0, 9)
                    if self.play_labels[lbl_idx]['text'] == ' ':
                        self.play_labels[lbl_idx]['text'] = self.p2_mark

        self.whose_turn.set(f'Turn:\n{self.player1} plays {self.p1_mark}')

        app.update_idletasks()

    def turn_number(self) -> int:
        """
        Keep count of turns per game by counting play labels with
        a mark string in the label text.
         """
        turn = 0
        for lbl in self.play_labels:
            if lbl['text'] != ' ':
                turn += 1

        return turn

    def check_winner(self) -> None:
        """
        Check each player's played mark (play_labels's text value) and
        evaluate whether played marks match a positional win in the
        board matrix (based on play_labels index values).
        In Player1 vs Player2 mode, which player goes first alternates
        with each game.
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

        for mark in (self.p1_mark, self.p2_mark):
            # Loop breaks when a winner is found b/c of calls to other functions.
            for combo in winning_combos:
                _x, _y, _z = combo
                lbl_x_txt = self.play_labels[_x]['text']
                lbl_y_txt = self.play_labels[_y]['text']
                lbl_z_txt = self.play_labels[_z]['text']

                if lbl_x_txt == lbl_y_txt == lbl_z_txt == mark:
                    self.winner_found = True

                    if self.mode_selection.get() in 'random, competitive':
                        award_points(mark)
                        self.auto_flash(combo, mark)
                    elif self.mode_selection.get() == 'pvpc':
                        award_points(mark)
                        self.flash_win(combo)
                        self.display_result(f'{mark} WINS!')

                    elif self.mode_selection.get() == 'pvp':
                        # Player2 is playing p1_mark on even game numbers, so
                        #   award p1_mark win to P2.
                        if self.num_game % 2 == 0:
                            if mark == self.p1_mark:
                                self.p2_points += 1
                            else:
                                self.p1_points += 1
                        else:
                            award_points(mark)

                        # After a PvP game, switch player label of whose_turn
                        #    to play the other mark (p1_mark always plays first).
                        self.player1, self.player2 = self.player2, self.player1

                        self.flash_win(combo)
                        self.display_result(f'{mark} WINS!')

                    self.num_game += 1

        if self.turn_number() == 9 and not self.winner_found:
            self.winner_found = True

            self.p1_points += 0.5
            self.p2_points += 0.5
            self.num_game += 1

            if self.mode_selection.get() in 'random, competitive':
                self.auto_flash((4, 4, 4), 'TIE')
            else:
                self.show_tie()
                self.display_result('IT IS A TIE!')

    def flash_win(self, combo) -> None:
        """
        Flashes the three winning squares, in series.
        Based on Bryan Oakley's answer for
        how-to-make-a-button-flash-using-after-in-tkinter
        https://stackoverflow.com/a/57298778
        """
        _x, _y, _z = combo

        app.after(10, lambda: self.play_labels[_x].config(bg=self.color['sq_won']))
        app.after(150, lambda: self.play_labels[_y].config(bg=self.color['sq_won']))
        app.after(300, lambda: self.play_labels[_z].config(bg=self.color['sq_won']))
        # app.after(300, lambda: self.play_labels[_z].config(bg=self.color['sq_not_won']))
        # app.after(400, lambda: self.play_labels[_y].config(bg=self.color['sq_not_won']))
        # app.after(500, lambda: self.play_labels[_x].config(bg=self.color['sq_not_won']))
        # app.after(600, lambda: self.play_labels[_x].config(bg=self.color['sq_won']))
        # app.after(600, lambda: self.play_labels[_y].config(bg=self.color['sq_won']))
        # app.after(600, lambda: self.play_labels[_z].config(bg=self.color['sq_won']))

    def show_tie(self):
        """
        Make game board blue on tie.
        """
        for lbl in self.play_labels:
            lbl.config(bg=self.color['sq_won'])
            app.update_idletasks()

    def flash_tie(self):
        """
        Flash the game board once and announce tie in center square.
        """
        def flash_blue():
            for lbl in self.play_labels:
                lbl.config(bg=self.color['blue'])
                app.update_idletasks()

        def tie_blue():
            for lbl in self.play_labels:
                lbl.config(text=' ')
            self.play_labels[4].config(text='TIE', bg=self.color['sq_won'])
            self.play_labels[4].config(text='TIE', bg=self.color['sq_won'])
            self.play_labels[4].config(text='TIE', bg=self.color['sq_won'])

        def tie_black():
            for lbl in self.play_labels:
                lbl.config(bg=self.color['sq_not_won'])
                app.update_idletasks()

        app.after(10, flash_blue)
        app.after(300, tie_blue)
        app.after(500, tie_black)

    def block_mode_switch(self) -> None:
        """
        Cancel/ignore an errant/mistimed play mode selection.
        Called from command of play mode Radiobuttons.
        Block any mode change if in the middle of a game.
        """

        if self.turn_number() > 0:
            if self.mode_selection.get() == 'pvp':
                self.mode_selection.set('pvpc')
            elif self.mode_selection.get() == 'pvpc':
                self.mode_selection.set('pvp')
            elif self.mode_selection.get() in 'random, competitive':
                # Set to default because don't know prior mode.
                self.pvp_mode.select()

            messagebox.showinfo(title='Mode unavailable',
                                detail='Finish this game,\n'
                                       'then change the play mode.')

    def block_playaction(self) -> None:
        """
        When autoplay is active, revent user action on play squares.
        """
        for lbl in self.play_labels:
            lbl.unbind('<Button-1>')
            lbl.unbind('<Enter>')
            lbl.unbind('<Leave>')

    def block_all_player_action(self) -> None:
        """
        Prevent user action in app window while display_result() window
        is open.
        """
        for lbl in self.play_labels:
            lbl.unbind('<Button-1>')
            lbl.unbind('<Enter>')
            lbl.unbind('<Leave>')

        self.quit_button.config(state=tk.DISABLED)
        self.auto_go_stop_rbtn.config(state=tk.DISABLED)

    def display_result(self, win_msg: str) -> None:
        """
        Create pop-up window to announce winner, tie, or halted autoplay.
        Provide option buttons to play again or quit app.
        Tally players' wins across re-plays and new games.

        :param win_msg: The result string to display in window.

        """

        result_window = tk.Toplevel(self, borderwidth=4, relief='raised')
        result_window.title('Game Report')
        result_window.geometry(
            f'250x125+{app.winfo_x() + 420}+{app.winfo_y() - 37}')
        result_window.config(bg=self.color['result_bg'])

        result_lbl = tk.Label(result_window, text=win_msg,
                              font=self.font['head14boldital'],
                              bg=self.color['result_bg'])

        self.block_all_player_action()
        self.whose_turn.set('Turn:\npending...')

        # Need to update players' cumulative wins in the app window.
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        # Need to unset autoplay mode to allow play action in Player modes:
        #   set to default PvP mode.
        if self.mode_selection.get() in 'random, competitive':
            self.pc_rando_mode.deselect()
            self.pc_compet_mode.deselect()
            self.pvp_mode.select()

        def enable_app_quit():
            """
            Need to enable app window Quit button if user closes
            Toplevel with the system's close window button.
            """
            self.quit_button.config(state=tk.NORMAL, command=quit_game)
            result_window.destroy()

        result_window.protocol('WM_DELETE_WINDOW', enable_app_quit)

        def new_game():
            self.reset_board()
            self.whose_turn.set(f'Turn:\n{self.player1} plays {self.p1_mark}')
            self.quit_button.config(state=tk.NORMAL, command=quit_game)
            self.auto_go_stop.set('Start autoplay')
            self.auto_go_stop_rbtn.config(state=tk.NORMAL)

            self.auto_turns_header.grid_remove()
            self.auto_turns_lbl.grid_remove()

            self.winner_found = False
            result_window.destroy()

        again = tk.Button(result_window, text='New Game', command=new_game)
        not_again = tk.Button(result_window, text='Quit', command=quit_game)

        result_lbl.pack(pady=3)
        again.pack(pady=5)
        not_again.pack()

    def auto_ctrl(self):
        """
        Check that an autoplay mode is selected before calling
        auto_start() when the auto_go_stop_rbtn Radiobutton is clicked.
        Called from the command function of auto_go_stop_rbtn.
        """
        if 'Start' in self.auto_go_stop.get():
            if self.mode_selection.get() in 'random, competitive':
                self.auto_go_stop.set('Stop autoplay')
                self.autoplay_on.set(True)
                self.auto_start()
            else:
                messagebox.showinfo(message='Autoplay mode not selected',
                                    detail='Play your turn or select\n'
                                           'an autoplay option when the\n'
                                           'current game is finished.')
                self.auto_go_stop.set('Start autoplay')
                self.autoplay_on.set(False)

        else:
            self.auto_go_stop.set('Start autoplay')
            self.autoplay_on.set(False)
            self.auto_stop()

    def auto_start(self) -> None:
        """
        Set starting values for autoplay and disable game modes when
        autoplay is in progress.
        """
        self.reset_board()
        self.whose_turn.set('PC autoplay')
        self.auto_turns_header.grid(row=0, column=2, rowspan=2,
                                    padx=(0, 15), pady=(15, 0), sticky=tk.E)
        self.auto_turns_lbl.grid(row=0, column=2, rowspan=2,
                                 padx=(0, 15), pady=(0, 15), sticky=tk.E)
        self.auto_go_stop_rbtn.config(state=tk.NORMAL)

        self.auto_turn_limit()
        self.auto_setup()
        # Start repeating calls to one of the autoplay methods;
        #   calls are controlled by after_id.
        if self.mode_selection.get() == 'random':
            self.autoplay_random()
        elif self.mode_selection.get() == 'competitive':
            self.autoplay_competitive()

    def auto_stop(self) -> None:
        """
        Stop autoplay method and call Results popup window.
        Disable player game actions (resets when Results window closes).
        """
        if self.after_id:
            app.after_cancel(self.after_id)
            self.after_id = None

        self.reset_board()
        self.display_result('Autoplay stopped')

    def auto_setup(self) -> None:
        """
        Run at the start of every new autoplay game. Update cumulative
        scores in the app window. Clear all marks from the board.
        """
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        self.winner_found = False

        self.reset_board()
        self.block_playaction()

    def auto_turn_limit(self) -> None:
        """
        Provide for 1000 alternating X & O autoplay turns; ~120-140 games.
        """
        # String of player marks is shortened one character per turn played.
        all_x = self.p1_mark * 500
        all_o = self.p2_mark * 500

        self.all_autoplay_marks = ''.join(map(lambda x, o: x + o, all_x, all_o))

    def autoplay_random(self) -> None:
        """
        Automatically play computer vs. computer for 1000 turns
        (~130 games) or until stopped by user. Each turn is played on a
        timed interval set by the self.auto_after time used in the
        after_id caller, so one turn per call. Alternate which player
        goes first in each game. Plays are random.
        """
        self.auto_turns_remaining.set(len(self.all_autoplay_marks))
        current_turn = self.turn_number()

        if len(self.all_autoplay_marks) > 0:
            mark = self.all_autoplay_marks[0]
            while current_turn == self.turn_number():
                lbl_idx = random.randrange(0, 9)
                if self.play_labels[lbl_idx]['text'] == ' ':
                    self.play_labels[lbl_idx]['text'] = mark

            if self.turn_number() >= 5:
                self.check_winner()

            # Need to move to next mark for next turn.
            self.all_autoplay_marks = self.all_autoplay_marks.lstrip(mark)

            # Need a pause so user can see what plays were made and also
            #   allow auto_stop() to break the call cycle.
            self.after_id = app.after(self.auto_after, self.autoplay_random)
        else:
            self.auto_stop()

    def autoplay_competitive(self):
        """
        Automatically play computer vs. computer for 1000 turns
        (~120 games) or until stopped by user. Each turn is played on a
        timed interval set by the self.auto_after time used in the
        after_id caller, so one turn per call. Alternate which player
        goes first in each game. First game play is at random position,
        the rest follow rules prioritizing blocking over winning.
        """
        # Tuples of winning list indices for the play_labels board squares.
        winning_combos = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),  # diagonals
        )

        self.auto_turns_remaining.set(len(self.all_autoplay_marks))
        current_turn = self.turn_number()

        if len(self.all_autoplay_marks) > 0:
            mark = self.all_autoplay_marks[0]

            # NOTE: If make first play random AND don't force X to go first, then
            #   wins are very even.
            while current_turn == self.turn_number():
                for combo in winning_combos:
                    _x, _y, _z = combo
                    x_txt = self.play_labels[_x]['text']
                    y_txt = self.play_labels[_y]['text']
                    z_txt = self.play_labels[_z]['text']
                    self.p2_mark, self.p1_mark = self.p1_mark, self.p2_mark
                    if current_turn == self.turn_number():
                        if x_txt == y_txt == self.p1_mark and z_txt == ' ':
                            self.play_labels[_z]['text'] = mark
                        elif y_txt == z_txt == self.p1_mark and x_txt == ' ':
                            self.play_labels[_x]['text'] = mark
                        elif x_txt == z_txt == self.p1_mark and y_txt == ' ':
                            self.play_labels[_y]['text'] = mark
                        elif x_txt == y_txt == self.p2_mark and z_txt == ' ':
                            self.play_labels[_z]['text'] = mark
                        elif y_txt == z_txt == self.p2_mark and x_txt == ' ':
                            self.play_labels[_x]['text'] = mark
                        elif x_txt == z_txt == self.p2_mark and y_txt == ' ':
                            self.play_labels[_y]['text'] = mark
                if current_turn == self.turn_number():
                    lbl_idx = random.randrange(0, 9)
                    if self.play_labels[lbl_idx]['text'] == ' ':
                        self.play_labels[lbl_idx]['text'] = mark

            if self.turn_number() >= 5:
                self.check_winner()

            # Need to move to next mark for next turn.
            self.all_autoplay_marks = self.all_autoplay_marks.lstrip(mark)

            # Need a pause so user can see what plays were made and also
            #   allow auto_stop() to break the call cycle.
            self.after_id = app.after(self.auto_after, self.autoplay_competitive)
        else:
            self.auto_stop()

    def auto_flash(self, combo: tuple, mark: str) -> None:
        """
        For each auto_play win, flashes the winning marks. Flashes the
        center square only on a tie (using combo = (4, 4, 4)), then
        calls auto_setup() for the next auto_play() game.

        :param combo: The tuple index values for a square on the board.
        :param mark: The player mark, usually 'X' or 'O', but can be any
                     string.
        """
        _x, _y, _z = combo

        def winner_show():
            self.play_labels[_x].config(text=mark, bg=self.color['sq_won'])
            self.play_labels[_y].config(text=mark, bg=self.color['sq_won'])
            self.play_labels[_z].config(text=mark, bg=self.color['sq_won'])
            app.update_idletasks()

        def winner_erase():
            self.play_labels[_x].config(text=' ', bg=self.color['sq_not_won'])
            self.play_labels[_y].config(text=' ', bg=self.color['sq_not_won'])
            self.play_labels[_z].config(text=' ', bg=self.color['sq_not_won'])

        app.after(10, winner_show)
        app.after(200, winner_erase)
        self.auto_setup()


if __name__ == '__main__':
    try:
        print('tty.py now running...')
        app = TicTacToeGUI()
        app.title('TIC TAC TOE')
        app.resizable(False, False)
        app.mainloop()

    except KeyboardInterrupt:
        print("*** User quit the program ***\n")
        sys.exit()

    except Exception as unknown:
        print(f'\nAn unexpected error: {unknown}\n')
        sys.exit()

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
    from tkinter import messagebox, ttk
except (ImportError, ModuleNotFoundError) as error:
    print(f'This program requires tkinter, which is included with \n'
          'Python 3.7+ distributions.\n'
          'Install the most recent version or re-install Python and include Tk/Tcl.\n'
          '\nOn Linux, you may also need: $ sudo apt-get install python3-tk\n'
          f'See also: https://tkdocs.com/tutorial/install.html \n{error}')


def quit_game(quit_now=True):
    """
    Manage app window Quit button. Ask for confirmation if a game has
    not yet finished.
    """
    if quit_now:
        app.destroy()
    else:
        msg = messagebox.askquestion(
            'Confirm', 'Current game is in play.\nQuit now?')
        if msg:
            app.destroy()


class TicTacToeGUI(tk.Tk):
    """Display the GUI playing board and control buttons."""

    def __init__(self):
        super().__init__()

        self.player1 = 'PLAYER 1'
        self.player2 = 'PLAYER 2'
        self.p1_mark = 'X'
        self.p2_mark = 'O'
        self.p1_points = 0
        self.p2_points = 0
        self.p1_score = tk.IntVar()
        self.p2_score = tk.IntVar()
        self.play_pc_ckb = tk.Checkbutton()
        self.play_pc = tk.BooleanVar()
        self.play_auto = tk.BooleanVar()
        self.after_id = None
        self.winner_found = False
        self.auto_after = 600  # ms, pause between turns for auto and PC modes.
        self.autoplay_marks = ''
        self.auto_turns = tk.IntVar()

        # Foreground and background colors.
        self.score_fg = 'DodgerBlue4'
        self.flash_on = 'blue'
        self.flash_off = 'black'

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
        self.play_btns = []
        self.pc_vs_pc_lbl = tk.Label()
        self.auto_start_btn = tk.Radiobutton()
        self.auto_stop_btn = tk.Radiobutton()
        self.quit_button = tk.Button()

        self.configure_widgets()
        self.grid_widgets()

    def configure_widgets(self) -> None:
        """Initial configurations for app window widgets."""
        # Player's turn widgets.
        self.whose_turn_lbl = tk.Label(textvariable=self.whose_turn, height=4,
                                       font=('TkHeadingFont', 11, 'italic bold'))
        self.whose_turn.set(f'Turn: {self.player1}, {self.p1_mark}')
        self.auto_turns_header = tk.Label(text='Turns remaining',
                                          font=('TkTooltipFont', 9))
        self.auto_turns_lbl = tk.Label(textvariable=self.auto_turns,
                                       font=('TkTooltipFont', 9),)

        # Players' scores widgets.
        # ︴symbol from https://coolsymbol.com/line-symbols.html
        self.score_header = tk.Label(
            text='Scores ︴', font=('TkHeadingFont', 12, 'bold'), fg=self.score_fg)
        self.player1_header = tk.Label(
            text='Player 1:', font=('TkHeaderFont', 10, 'bold'), fg=self.score_fg)
        self.player2_header = tk.Label(
            text='Player 2:', font=('TkHeaderFont', 10, 'bold'), fg=self.score_fg)
        self.player1_score_lbl = tk.Label(
            textvariable=self.p1_score, font=('TkHeaderFont', 12, 'bold'),
            fg=self.score_fg)
        self.player2_score_lbl = tk.Label(
            textvariable=self.p2_score, font=('TkHeaderFont', 12, 'bold'),
            fg=self.score_fg)

        # Play action widgets.
        # play_btns help from https://stackoverflow.com/questions/54979853/
        #    tic-tac-toe-using-python-tkinter
        # ..and https://stackoverflow.com/questions/10865116/
        #    tkinter-creating-buttons-in-for-loop-passing-command-arguments
        self.play_btns = [tk.Button(command=lambda curr_btn=i: self.player_turn(
            self.play_btns[curr_btn])) for i in range(9)]
        for btn in self.play_btns:
            btn.config(text=' ', height=3, width=5,
                       bg=self.flash_off, fg='yellow2',
                       font='TkFixedFont 30 bold',
                       activebackground='grey15',
                       activeforeground='yellow3',
                       disabledforeground='yellow3',
                       highlightthickness=6,
                       )

        # Play computer option is enabled at start of game and any time
        #   following Player2's turn in Player vs Player mode;
        #   play_pc_ckb is disabled all other times.
        self.play_pc_ckb.config(text='Play computer',
                                variable=self.play_pc,
                                borderwidth=0,
                                font=('TkDefaultFont', 10, 'bold'))
        self.pc_vs_pc_lbl = tk.Label(text='PC vs. PC',
                                     font=('TkDefaultFont', 10, 'bold'))

        self.auto_start_btn = tk.Radiobutton(text='Start', value=1,
                                             variable=self.play_auto,
                                             width=5,
                                             command=self.auto_start,
                                             borderwidth=3,
                                             indicatoron=False,
                                             )
        self.auto_stop_btn = tk.Radiobutton(text='Stop', value=0,
                                            variable=self.play_auto,
                                            width=5,
                                            command=self.auto_stop,
                                            borderwidth=3,
                                            indicatoron=False,
                                            state='disabled',
                                            )

        self.quit_button = tk.Button(text='Quit', command=quit_game)

    def grid_widgets(self) -> None:
        """Position app window widgets. Configure play buttons."""

        # Position play action buttons in 3 x 3 grid. Note that while
        #   nothing is gridded in row index 1, the top row uses rowspan=2
        #   to center widgets vertically; hence, play buttons begin on
        #   row index 2.
        _row = 2
        _col = 0
        for btn in self.play_btns:
            btn.grid(column=_col, row=_row)
            _col += 1
            if _col > 2:
                _col = 0
                _row += 1

        # Squeeze everything in with pretty spanning, padding, and stickies.
        self.whose_turn_lbl.grid(row=0, column=0, padx=(8, 0), sticky=tk.W)

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

        self.play_pc_ckb.grid(row=5, column=0,
                              pady=5, sticky=tk.EW)
        self.pc_vs_pc_lbl.grid(row=5, column=1,
                               padx=(20, 0), pady=5, sticky=tk.W)
        self.auto_start_btn.grid(row=5, column=1,
                                 padx=(0, 22), pady=(0, 30), sticky=tk.E)
        self.auto_stop_btn.grid(row=5, column=1,
                                padx=(0, 22), pady=(25, 0), sticky=tk.E)

        self.quit_button.grid(row=5, column=2,
                              padx=(0, 15), pady=(5, 8), sticky=tk.E)

    def player_turn(self, played_btn: tk) -> None:
        """
        Check whether square (button) selected by players, *played_btn*,
        is available to play either 'X' or 'O'.
        Assign player's mark to text value of the selected button.
        Reply to played button with computer's turn if option selected.
        Evaluate players' turns for a win after 5th turn.

        :param played_btn: The tk.Button object that was clicked.
        """
        # Need to disable auto_play() mode until current game is over.
        self.auto_start_btn.config(state='disabled')
        self.pc_vs_pc_lbl.config(fg='grey65')

        # Note: X (human) always plays first.
        if played_btn['text'] == ' ':
            if self.play_pc.get():
                if self.turn_number() % 2 == 0:
                    played_btn['text'] = self.p1_mark
                    self.whose_turn.set(f'Turn: COMPUTER, {self.p2_mark}')

                    # Need update to see the pc_turn() play delayed by app.after.
                    app.update_idletasks()

                    if self.turn_number() >= 5:
                        self.check_winner()

                    if self.turn_number() < 9 and not self.winner_found:
                        self.pc_turn()

                        if self.turn_number() >= 5:
                            self.check_winner()

                        self.play_pc_ckb.config(state='normal')
            else:
                if self.turn_number() % 2 == 0:
                    played_btn['text'] = self.p1_mark
                    self.whose_turn.set(f'Turn: {self.player2}, {self.p2_mark}')
                    self.play_pc_ckb.config(state='disabled')
                else:
                    played_btn['text'] = self.p2_mark
                    self.whose_turn.set(f'Turn: {self.player1}, {self.p1_mark}')
                    self.play_pc_ckb.config(state='normal')

                if self.turn_number() >= 5:
                    self.check_winner()
        else:
            messagebox.showerror('Oops!', 'This square was already played!')

        self.quit_button.config(command=lambda: quit_game(False))

    def pc_turn(self):
        """
        Computer plays Player2. Play the center square if open, otherwise
        block any two Xs in a row; if none, then randomly play first
        available square. Algorithm favors blocking over winning to
        counter X's advantage of playing first.
        """
        # Delay play for a better feel.
        #   With this, need app.update_idletasks() after Player 1 plays.
        app.after(self.auto_after)

        # Initial idea for algorithm:
        # https://www.simplifiedpython.net/python-tic-tac-toe-using-artificial-intelligence/
        winning_combos = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),  # diagonals
        )

        pc_turn = self.turn_number()

        while pc_turn == self.turn_number():
            if self.play_btns[4]['text'] == ' ':
                self.play_btns[4]['text'] = self.p2_mark

            else:
                # combo loop is broken when p2_mark is played, adding a turn.
                #  If no play in loop, then play a random open square.
                for combo in winning_combos:
                    _x, _y, _z = combo
                    x_txt = self.play_btns[_x]['text']
                    y_txt = self.play_btns[_y]['text']
                    z_txt = self.play_btns[_z]['text']

                    if pc_turn == self.turn_number():
                        if x_txt == y_txt == "X" and z_txt == ' ':
                            self.play_btns[_z]['text'] = self.p2_mark
                        elif y_txt == z_txt == self.p1_mark and x_txt == ' ':
                            self.play_btns[_x]['text'] = self.p2_mark
                        elif x_txt == z_txt == self.p1_mark and y_txt == ' ':
                            self.play_btns[_y]['text'] = self.p2_mark
                        elif x_txt == y_txt == "O" and z_txt == ' ':
                            self.play_btns[_z]['text'] = self.p2_mark
                        elif y_txt == z_txt == self.p2_mark and x_txt == ' ':
                            self.play_btns[_x]['text'] = self.p2_mark
                        elif x_txt == z_txt == self.p2_mark and y_txt == ' ':
                            self.play_btns[_y]['text'] = self.p2_mark

                if pc_turn == self.turn_number():
                    move = random.randrange(0, 9)
                    if self.play_btns[move]['text'] == ' ':
                        self.play_btns[move]['text'] = self.p2_mark

        self.whose_turn.set(f'Turn: {self.player1}, {self.p1_mark}')

        app.update_idletasks()

    def turn_number(self) -> int:
        turn = 0
        for btn in self.play_btns:
            if btn['text'] != ' ':
                turn += 1

        return turn

    def check_winner(self) -> None:
        """
        Check each player's played mark (play_btns's text value) and
        evaluate whether played marks match a positional win in the
        board matrix (based on play_btns index values).
        In Player vs Player mode, which player goes first alternates
        with each game.
        """
        winning_combos = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),  # diagonals
        )

        for mark in (self.p1_mark, self.p2_mark):
            # Loop breaks when a winner is found b/c of calls to other functions.
            for combo in winning_combos:
                _x, _y, _z = combo
                btn_x_txt = self.play_btns[_x]['text']
                btn_y_txt = self.play_btns[_y]['text']
                btn_z_txt = self.play_btns[_z]['text']

                if btn_x_txt == btn_y_txt == btn_z_txt == mark:
                    self.winner_found = True

                    if mark == self.p1_mark:
                        self.p1_points += 1
                    else:
                        self.p2_points += 1

                    if self.play_auto.get():
                        self.auto_flash(combo, mark)
                    elif self.play_pc.get():
                        self.flash_win(combo)
                        self.block_player_action()
                        self.display_result(f'{mark} WINS!')
                    else:
                        self.flash_win(combo)
                        self.block_player_action()
                        self.player1, self.player2 = self.player2, self.player1
                        self.display_result(f'{mark} WINS!')

        if self.turn_number() == 9 and not self.winner_found:
            self.winner_found = True

            self.p1_points += 0.5
            self.p2_points += 0.5

            if self.play_auto.get():
                self.auto_flash((4, 4, 4), 'TIE')
            else:
                # self.flash_tie()
                # TODO: Consider whether to leave all marks up in blue
                #  (no flash) or flash, remove marks, and announce TIE.
                self.show_tie()
                self.block_player_action()
                self.display_result('IT IS A TIE!')

    def flash_win(self, combo) -> None:
        """
        Flashes the three winning squares, in series.
        Based on Bryan Oakley's answer for
        how-to-make-a-button-flash-using-after-in-tkinter
        https://stackoverflow.com/a/57298778
        """
        _x, _y, _z = combo
        # app.after(10, lambda: self.play_btns[_x].config(bg=self.flash_on))
        # app.after(300, lambda: self.play_btns[_x].config(bg=self.flash_off))
        # app.after(100, lambda: self.play_btns[_y].config(bg=self.flash_on))
        # app.after(400, lambda: self.play_btns[_y].config(bg=self.flash_off))
        # app.after(200, lambda: self.play_btns[_z].config(bg=self.flash_on))
        # app.after(500, lambda: self.play_btns[_z].config(bg=self.flash_off))

        # app.after(10, lambda: self.play_btns[_x].config(bg=self.flash_on))
        # app.after(200, lambda: self.play_btns[_y].config(bg=self.flash_on))
        # app.after(400, lambda: self.play_btns[_z].config(bg=self.flash_on))

        app.after(10, lambda: self.play_btns[_x].config(bg=self.flash_on))
        app.after(100, lambda: self.play_btns[_y].config(bg=self.flash_on))
        app.after(200, lambda: self.play_btns[_z].config(bg=self.flash_on))
        app.after(300, lambda: self.play_btns[_z].config(bg=self.flash_off))
        app.after(400, lambda: self.play_btns[_y].config(bg=self.flash_off))
        app.after(500, lambda: self.play_btns[_x].config(bg=self.flash_off))
        app.after(600, lambda: self.play_btns[_x].config(bg=self.flash_on))
        app.after(600, lambda: self.play_btns[_y].config(bg=self.flash_on))
        app.after(600, lambda: self.play_btns[_z].config(bg=self.flash_on))

    def show_tie(self):
        """
        Make game board blue on tie.
        """
        for btn in self.play_btns:
            btn.config(bg=self.flash_on)
            app.update_idletasks()

    def flash_tie(self):
        """
        Flash the game board once and announce tie in center square.
        """
        def flash_blue():
            for btn in self.play_btns:
                btn.config(bg=self.flash_on)
                app.update_idletasks()

        def tie_blue():
            for btn in self.play_btns:
                btn.config(text=' ')
            self.play_btns[4].config(text='TIE', bg=self.flash_on)
            self.play_btns[4].config(text='TIE', bg=self.flash_on)
            self.play_btns[4].config(text='TIE', bg=self.flash_on)

        def tie_black():
            for btn in self.play_btns:
                btn.config(bg=self.flash_off)
                app.update_idletasks()

        app.after(10, flash_blue)
        app.after(300, tie_blue)
        app.after(600, tie_black)

    def block_player_action(self) -> None:
        """
        Prevent user action in app window while display_result() window
        is open.
        """
        for btn in self.play_btns:
            btn.config(state='disabled')
        self.play_pc_ckb.config(state='disabled')
        self.quit_button.config(state='disabled')

    def display_result(self, win_msg: str) -> None:
        """
        Create pop-up window to announce winner, tie, or halted autoplay.
        Provide option buttons to play again or quit app.
        Tally players' wins across re-plays and new games.

        :param win_msg: The result string to display in window.

        """
        self.whose_turn.set('Turn: pending...')

        result_window = tk.Toplevel(self, borderwidth=4, relief='raised')
        result_window.title('Game Report')
        result_window.geometry(
            f'225x125+{app.winfo_x() + 420}+{app.winfo_y() - 37}')
        result_window.config(bg='Yellow3')

        def enable_app_quit():
            """
            Need to enable app window Quit button if user closes
            Toplevel with the system's close window button.
            """
            self.quit_button.config(state='normal', command=quit_game)
            result_window.destroy()

        result_window.protocol('WM_DELETE_WINDOW', enable_app_quit)

        def new_game():
            for btn in self.play_btns:
                btn.config(text=' ', state='normal', bg=self.flash_off)
            self.whose_turn.set(f'Turn: {self.player1}, {self.p1_mark}')
            self.play_pc_ckb.config(state='normal')
            self.quit_button.config(state='normal', command=quit_game)
            self.auto_start_btn.config(state='normal')
            self.pc_vs_pc_lbl.config(fg='black')

            self.auto_turns_header.grid_remove()
            self.auto_turns_lbl.grid_remove()

            self.winner_found = False
            result_window.destroy()

        result_lbl = tk.Label(result_window, text=win_msg,
                              font=('TkHeadingFont', 14, 'bold italic'),
                              bg='Yellow3')

        again = tk.Button(result_window, text='New Game', command=new_game)
        not_again = tk.Button(result_window, text='Quit', command=quit_game)

        result_lbl.pack(pady=3)
        again.pack(pady=5)
        not_again.pack()

        # Need to update players' cumulative wins in the app window.
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

    def auto_start(self) -> None:
        """Block user game actions and set starting values."""

        self.whose_turn.set('PC autoplay')
        for btn in self.play_btns:
            btn.config(state='disabled')
        self.play_pc_ckb.config(state='disabled')
        self.auto_start_btn.config(state='disabled')
        self.auto_stop_btn.config(state='normal')
        self.auto_turns_header.grid(row=0, column=2, rowspan=2,
                                    padx=(0, 15), pady=(15, 0), sticky=tk.E)
        self.auto_turns_lbl.grid(row=0, column=2, rowspan=2,
                                 padx=(0, 15), pady=(0, 15), sticky=tk.E)

        self.auto_limit()
        self.auto_setup()

        # Start repeating calls to auto_play(); controlled by after_id.
        self.auto_play()

    def auto_stop(self) -> None:
        """Stop auto_play(); call Results popup window. Disable player
        game actions.
        """
        if self.after_id:
            app.after_cancel(self.after_id)
            self.after_id = None
        self.auto_start_btn.config(state='disabled')
        self.auto_stop_btn.config(state='disabled')
        self.pc_vs_pc_lbl.config(fg='grey65')

        self.display_result('PC vs PC stopped')

    def auto_setup(self) -> None:
        """
        Run at the start of every new auto_play game. Update cumulative
        scores in the app window. Clear all marks from the board.
        Ensure that new games start with X.
        """
        self.p1_score.set(self.p1_points)
        self.p2_score.set(self.p2_points)

        self.winner_found = False

        for btn in self.play_btns:
            btn.config(text=' ')

        mark = self.autoplay_marks[0]
        if mark == self.p2_mark:
            self.autoplay_marks = self.autoplay_marks.lstrip(mark)

    def auto_limit(self) -> None:
        """
        Provide for about 1840 alternating X & O auto_play flags; about
        240 games. Start with 2000 flags because games need to start
        with 'X', so leading 'O' may be striped from marks string at the
        start of new games.
        """
        # Need to limit auto_play() turns. String of 2000 text marks
        #   is shortened one character each turn. Actual number of
        #   turns will be ~9% less b/c new games always start with 'X'
        #   by stripping any leading 'O'.
        k_x = self.p1_mark * 1000
        k_o = self.p2_mark * 1000
        self.autoplay_marks = ''.join(map(lambda x, o: x + o, k_x, k_o))

    def auto_play(self) -> None:
        """
        Automatically play computer vs. computer for ~1840 turns
        (~240 games) or until stopped by user. Each turn is played on a
        timed interval set by the self.auto_after time used in the
        after_id caller. Plays are random except for priority of placing
        O' in the center square at first opportunity; this reduces X's
        first play advantage to ~1.2x.
        """
        self.auto_turns.set(len(self.autoplay_marks))
        current_turn = self.turn_number()

        if len(self.autoplay_marks) >= 1:
            mark = self.autoplay_marks[0]
            self.autoplay_marks = self.autoplay_marks.lstrip(mark)

            if mark == self.p2_mark and self.play_btns[4]['text'] == ' ':
                self.play_btns[4]['text'] = mark
            else:
                while current_turn == self.turn_number():
                    move = random.randrange(0, 9)
                    if self.play_btns[move]['text'] == ' ':
                        self.play_btns[move]['text'] = mark

            if self.turn_number() >= 5:
                self.check_winner()

            # Need a pause so user can see what plays were made and also
            #   allow auto_stop() to break the call cycle.
            self.after_id = app.after(self.auto_after, self.auto_play)
        else:
            self.auto_stop_btn.invoke()  # alt: self.auto_stop()

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

        def winner_blue():
            self.play_btns[_x].config(text=mark, bg=self.flash_on)
            self.play_btns[_y].config(text=mark, bg=self.flash_on)
            self.play_btns[_z].config(text=mark, bg=self.flash_on)
            app.update_idletasks()

        def winner_erase():
            self.play_btns[_x].config(text=' ', bg=self.flash_off)
            self.play_btns[_y].config(text=' ', bg=self.flash_off)
            self.play_btns[_z].config(text=' ', bg=self.flash_off)

        app.after(10, winner_blue)
        app.after(400, winner_erase)
        self.auto_setup()


if __name__ == '__main__':
    app = TicTacToeGUI()
    app.title('TIC TAC TOE')
    app.resizable(False, False)
    app.mainloop()

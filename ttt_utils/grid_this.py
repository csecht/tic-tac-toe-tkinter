"""
Assign widget grids and padding for individual platforms; Linux, MacOS,
or Windows.
Functions: linux, mac, windows
Each function takes as a parameter the name of the grid parent,
generally the mainloop tk window (root, app, etc.) or the Frame that
fills the main tk window.
"""
# Copyright (C) 2022 C.S. Echt under MIT License'

from tkinter import E, W, EW, NE, SE


# Grid statements are sorted by row, then column.
# Differences in grid values in general depend on font pixel width
#   and default font differences among platforms.

def linux(parent):
    parent.whose_turn_lbl.grid(
        row=0, column=0,
        padx=(12, 0), pady=(5, 0), sticky=W)
    parent.prev_game_num_header.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(8, 0), sticky=NE)
    parent.prev_game_num_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(22, 0), sticky=NE)
    parent.score_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(10, 0), pady=(0, 10), sticky=W)
    parent.player1_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 12), pady=(0, 35), sticky=E)
    parent.player2_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 12), pady=(20, 10), sticky=E)
    parent.player1_score_lbl.grid(
        row=0, column=1,
        rowspan=2, columnspan=2,
        padx=(112, 0), pady=(0, 35), sticky=W)
    parent.player2_score_lbl.grid(
        row=0, column=1, rowspan=2, columnspan=2,
        padx=(112, 0), pady=(20, 10), sticky=W)
    parent.auto_turns_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(0, 0), sticky=SE)
    parent.auto_turns_header.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(0, 16), sticky=SE)
    parent.ties_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 12), pady=(55, 0), sticky=E)
    parent.ties_lbl.grid(
        row=0, column=1,
        rowspan=2, columnspan=2,
        padx=(112, 0), pady=(55, 0), sticky=W)
    parent.pvp_mode.grid(
        row=5, column=0,
        padx=(10, 0), pady=5, sticky=W)
    parent.pvpc_mode.grid(
        row=5, column=1,
        columnspan=2,
        padx=(10, 0), pady=5, sticky=W)
    parent.choose_pc_pref.grid(
        row=5, column=1,
        columnspan=2,
        padx=(0, 25), pady=0, sticky=E)
    parent.separator.grid(
        row=7, column=0,
        columnspan=3,
        padx=10, sticky=EW)
    parent.auto_start_stop_btn.grid(
        row=8, column=1,
        rowspan=2,
        padx=(9, 0), pady=(6, 0), sticky=W)
    parent.autospeed_lbl.grid(
        row=8, column=1,
        rowspan=2, columnspan=2,
        padx=(0, 45), pady=(6, 0), sticky=E)
    parent.autospeed_fast.grid(
        row=9, column=1,
        columnspan=2,
        padx=(0, 90), pady=(16, 0), sticky=E)
    parent.autospeed_slow.grid(
        row=9, column=1,
        columnspan=2,
        padx=(0, 30), pady=(16, 0), sticky=E)
    parent.auto_random_mode.grid(
        row=8, column=0,
        padx=0, pady=(4, 0), sticky=W)
    parent.auto_center_mode.grid(
        row=9, column=0,
        padx=0, pady=0, sticky=W)
    parent.auto_tactics_mode.grid(
        row=10, column=0,
        padx=0, pady=0, sticky=W)
    parent.who_autostarts_btn.grid(
        row=11, column=0,
        columnspan=2,
        padx=(0, 17), pady=(0, 7), sticky=E)
    parent.quit_button.grid(
        row=11, column=2,
        padx=(0, 8), pady=(0, 7), sticky=E)


def mac(parent):
    parent.whose_turn_lbl.grid(
        row=0, column=0,
        padx=(5, 0), pady=(5, 0))
    parent.prev_game_num_header.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(8, 0), sticky=NE)
    parent.prev_game_num_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(22, 0), sticky=NE)
    parent.score_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 0), pady=(0, 10), sticky=W)
    parent.player1_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 13), pady=(0, 35), sticky=E)
    parent.player2_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 13), pady=(20, 10), sticky=E)
    parent.player1_score_lbl.grid(
        row=0, column=1,
        rowspan=2, columnspan=2,
        padx=(112, 0), pady=(0, 35), sticky=W)
    parent.player2_score_lbl.grid(
        row=0, column=1, rowspan=2, columnspan=2,
        padx=(112, 0), pady=(20, 10), sticky=W)
    parent.auto_turns_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(0, 0), sticky=SE)
    parent.auto_turns_header.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(0, 16), sticky=SE)
    parent.ties_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 13), pady=(55, 0), sticky=E)
    parent.ties_lbl.grid(
        row=0, column=1,
        rowspan=2, columnspan=2,
        padx=(112, 0), pady=(55, 0), sticky=W)
    parent.pvp_mode.grid(
        row=5, column=0,
        padx=(16, 0), pady=5, sticky=W)
    parent.pvpc_mode.grid(
        row=5, column=1,
        columnspan=2,
        padx=(16, 0), pady=5, sticky=W)
    parent.choose_pc_pref.grid(
        row=5, column=1,
        columnspan=2,
        padx=(0, 20), pady=0, sticky=E)
    parent.separator.grid(
        row=7, column=0,
        columnspan=3,
        padx=10, sticky=EW)
    parent.auto_start_stop_btn.grid(
        row=8, column=1,
        rowspan=2,
        padx=(9, 0), pady=(6, 0), sticky=W)
    parent.autospeed_lbl.grid(
        row=8, column=1,
        rowspan=2, columnspan=2,
        padx=(0, 50), pady=(6, 0), sticky=E)
    parent.autospeed_fast.grid(
        row=9, column=1, columnspan=2,
        padx=(0, 90), pady=(16, 0), sticky=E)
    parent.autospeed_slow.grid(
        row=9, column=1,
        columnspan=2,
        padx=(0, 30), pady=(16, 0), sticky=E)
    parent.auto_random_mode.grid(
        row=8, column=0,
        padx=(5, 0), pady=(4, 0), sticky=W)
    parent.auto_center_mode.grid(
        row=9, column=0,
        padx=(5, 0), pady=0, sticky=W)
    parent.auto_tactics_mode.grid(
        row=10, column=0,
        padx=(5, 0), pady=0, sticky=W)
    parent.who_autostarts_btn.grid(
        row=11, column=0,
        columnspan=2,
        padx=(0, 15), pady=(0, 7), sticky=E)
    parent.quit_button.grid(
        row=11, column=2,
        padx=(0, 8), pady=(0, 7), sticky=E)


def windows(parent):
    parent.whose_turn_lbl.grid(
        row=0, column=0,
        padx=0, pady=(5, 0))
    parent.prev_game_num_header.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(7, 0), sticky=NE)
    parent.prev_game_num_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(35, 0), sticky=NE)
    parent.score_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(10, 0), pady=(0, 10), sticky=W)
    parent.player1_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 8), pady=(0, 45), sticky=E)
    parent.player2_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 8), pady=(30, 10), sticky=E)
    parent.player1_score_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=0, pady=(0, 50), sticky=W)
    parent.player2_score_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=0, pady=(30, 10), sticky=W)
    parent.auto_turns_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(0, 0), sticky=SE)
    parent.auto_turns_header.grid(
        row=0, column=2,
        rowspan=2,
        padx=(0, 8), pady=(0, 30), sticky=SE)
    parent.ties_header.grid(
        row=0, column=1,
        rowspan=2,
        padx=(0, 8), pady=(90, 0), sticky=E)
    parent.ties_lbl.grid(
        row=0, column=2,
        rowspan=2,
        padx=0, pady=(90, 0), sticky=W)
    parent.pvp_mode.grid(
        row=5, column=0,
        padx=(25, 0), pady=5, sticky=W)
    parent.pvpc_mode.grid(
        row=5, column=1,
        columnspan=2,
        padx=(30, 0), pady=5, sticky=W)
    parent.choose_pc_pref.grid(
        row=5, column=1,
        columnspan=2,
        padx=(0, 45), pady=0, sticky=E)
    parent.separator.grid(
        row=7, column=0,
        columnspan=3,
        padx=10, sticky=EW)
    parent.auto_start_stop_btn.grid(
        row=8, column=1,
        rowspan=2,
        padx=(9, 0), pady=(6, 0), sticky=W)
    parent.autospeed_lbl.grid(
        row=8, column=2,
        rowspan=2,
        padx=(0, 0), pady=(0, 0), sticky=W)
    parent.autospeed_fast.grid(
        row=9, column=1,
        columnspan=2,
        padx=(180, 0), pady=(16, 0), sticky=W)
    parent.autospeed_slow.grid(
        row=9, column=1,
        columnspan=2,
        padx=(0, 80), pady=(16, 0), sticky=E)
    parent.auto_random_mode.grid(
        row=8, column=0,
        padx=(5, 0), pady=(4, 0), sticky=W)
    parent.auto_center_mode.grid(
        row=9, column=0,
        padx=(5, 0), pady=0, sticky=W)
    parent.auto_tactics_mode.grid(
        row=10, column=0,
        padx=(5, 0), pady=0, sticky=W)
    parent.who_autostarts_btn.grid(
        row=11, column=0,
        columnspan=2,
        padx=(0, 50), pady=(0, 7), sticky=E)
    parent.quit_button.grid(
        row=11, column=2,
        padx=(0, 8), pady=(0, 7), sticky=E)

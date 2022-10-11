# Project: tic-tac-toe-tkinter

![tic_tac_logo](images/Tic_tac_toe.png)

<sub>Image modified from https://en.wikipedia.org/wiki/File:Tic_tac_toe.svg</sub>

<sub>Game design inspired by Riya Tendulkar code:
https://levelup.gitconnected.com/how-to-code-tic-tac-toe-in-python-using-tkinter-e7f9ce510bfb
https://gist.github.com/riya1620/72c2b668ef29da061c44d97a82318572
</sub>

## A Tic Tak Toe Game in tkinter

Developed with Python 3.8, under Ubuntu 20.04, Windows 10 and macOS 10.13. Should work with Python 3.6.
Recent Python packages can be downloaded from https://www.python.org/downloads/.

### Usage: 
From a command line:
From within the tic-tac-toe-tk-main folder, from a Terminal or Command Prompt, depending on your system environment:

            python3 -m plot_jobs (recommended for all systems)
            py plot_jobs.py (Windows)
            python3 plot_jobs.py (Linux, Mac)
            ./plot_jobs.py (Linux, Mac)

### Play action
There are four play modes:
- Player vs Player
- Player vs PC (computer)
- Autoplay, random (computer plays itself randomly)
- Autoplay, center (like strategy, but 1st play in center)
- Autoplay, strategy (computer vs. itself with rules, 1st play random)

In Player v PC game mode, you can choose among computer play options:
- PC plays random
- PC plays center; prefers the center
- PC plays strategy; rules-based, hardest to beat

Wins, ties, and mode-specific PC moves are recorded in the Terminal window with "center" and "strategy" PC modes; this may help the human player to improve their game.

In Autoplay mode, the PC plays itself. You can choose to have Player 1 (X) start every game or have both Players alternate game starts. 1000 turns are played at about 3 turns per second. Scores are updated in realtime through the series of about 110 to 130 games. Studying autoplay results in different play modes can be instructive for improving your game strategies!

### Screenshots

Human (Player 1, X) wins 19th game in "PC plays center" mode. A Result pop-up window prompts user to play again or quit the program. The pop-up window can be repositioned.

![pvpc-game](images/X_wins_PvPC.png)

Autoplay game in progress with strategy mode, with PC players alternating start turns, 650 turns remaining, autoplay speed set to Slow, the default:

![autoplay-game](images/autoplay.png)

### Keyboard navigation

All actions that are done with the mouse can also be done with the keys. To play marks in squares, use either the numeric keypad or the nine letter keys on the left side of the keyboard. In both cases, the top row of keys corresponds to the top row of squares, following with the middle and bottom rows.

For example, with two people competing in Player v Player mode, one can use the mouse while the other uses the keyboard.

Modes and buttons can be selected by cycling through with the Tab key. Activate the desired mode by pressing Enter. The 'Player 1 starts' button in the lower left becomes selectable only when an Autoplay mode is active; toggle between 'Player 1 starts' and 'Players alternate' with the space bar.

Similarly, the space bar activates the Quit button once it has selection focus.

### Known Issues
Waiting for feedback...

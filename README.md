# py_wordle

## Run the game

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run
the game from the project directory:

```powershell
uv sync
uv run py_wordle.py
```

Use `-d` to print the secret word in the terminal for debugging:

```powershell
uv run py_wordle.py -d
```

The project requires Python 3.10 or newer. uv uses `pyproject.toml` and
`uv.lock` to manage the project environment and dependencies.

## How to play

Guess the hidden five-letter word in six attempts. Type letters to fill the
current row, then press **Enter** to submit a complete guess. Guesses must be
words in the game's word list. Incomplete guesses and words outside the list
show a message and are not submitted. Extra letters are ignored once the row
is full.

After a valid guess, the tile colors show how close you are:

- **Green**: the letter is in the word and in the correct position.
- **Yellow**: the letter is in the word but in a different position.
- **Gray**: the letter is not in the word.

Use **Backspace** to remove a letter from the current guess. The game ends when
you guess the word or use all six attempts. Press **Space** after the game ends
to start a new round. Closing the game window quits the game.

The game accepts five-letter words from SCOWL's standard British English
`-ise` dictionary. The possible answers are the existing answer list filtered
against that dictionary, so words outside its British English list—including
US spellings such as “fiber”—aren't accepted. See
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for the source and license.

Short synthesized sound effects play for typing, guesses, and game results. If
audio cannot be initialized on the system, the game continues without sound and
prints a warning.

Run the automated gameplay tests with:

```powershell
uv run python -m unittest discover -s tests -v
```

## Build the Windows executable

Run the build script from the project directory. It installs the build tools
with uv and creates `dist\wordle_main.exe`:

```powershell
.\build.ps1
```

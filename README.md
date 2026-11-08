# py_wordle

## Run the game

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run
the game from the project directory:

```powershell
uv sync
uv run py_wordle.py
```

The project requires Python 3.10 or newer. uv uses `pyproject.toml` and
`uv.lock` to manage the project environment and dependencies.

## How to play

Guess the hidden five-letter word in six attempts. Type letters to fill the
current row, then press **Enter** to submit a complete guess. Guesses must be
words in the game's word list; incomplete or unrecognized guesses are not
submitted.

After a valid guess, the tile colors show how close you are:

- **Green**: the letter is in the word and in the correct position.
- **Yellow**: the letter is in the word but in a different position.
- **Gray**: the letter is not in the word.

Use **Backspace** to remove a letter from the current guess. The game ends when
you guess the word or use all six attempts. Press **Space** after the game ends
to start a new round. Closing the game window quits the game.

The game accepts guesses from an expanded five-letter English word list, while
the original `wordlist.txt` remains the pool of possible answers. The expanded
list is filtered from the SCOWL/English Speller Database US-large dictionary;
see [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for its source and
license.

## Build the Windows executable

Run the build script from the project directory. It installs the build tools
with uv and creates `dist\wordle_main.exe`:

```powershell
.\build.ps1
```

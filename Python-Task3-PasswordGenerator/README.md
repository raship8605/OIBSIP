# Task 3 · Password Generator (Advanced)

Advanced-tier password generator built for the **Oasis Infobyte Python Programming Internship**.

## Features

- tkinter GUI with length slider and character-type checkboxes
- Uses `secrets` module (cryptographically secure — not `random`)
- Visual strength indicator: Very Weak / Weak / Medium / Strong / Very Strong
- Guarantees at least one character from each selected type
- "Copy to Clipboard" button (auto-copies on generation via `pyperclip`)
- Option to exclude ambiguous characters: `0 O l 1 I | ` ' "`
- Session history: last 5 generated passwords (not persisted to disk)

## Requirements

- Python 3.10+
- pyperclip (`pip install -r requirements.txt`)
- tkinter (bundled with Python)

## Run

```bash
pip install -r requirements.txt
python main.pys
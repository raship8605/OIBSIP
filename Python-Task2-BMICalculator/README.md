# Task 2 · BMI Calculator (Advanced)

Advanced-tier BMI Calculator built for the **Oasis Infobyte Python Programming Internship**.

## Features

- tkinter GUI (no command line)
- Weight + height input fields with a Calculate & Save button
- Colour-coded result (green = normal, red = obese, etc.)
- Multi-user support (named users)
- SQLite persistence (`bmi_records.db`)
- matplotlib trend line of a user's BMI over time
- Graceful error handling for bad input and DB failures

## Requirements

- Python 3.10+
- matplotlib (`pip install -r requirements.txt`)
- tkinter (bundled with Python)
- sqlite3 (bundled with Python)

## Run

```bash
pip install -r requirements.txt
python main.py
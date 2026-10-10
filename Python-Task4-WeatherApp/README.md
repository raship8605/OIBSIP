# Task 4 · Weather App (Advanced)

Advanced-tier weather app built for the **Oasis Infobyte Python Programming Internship**.

## Features

- tkinter GUI with city input, "Get Weather" button, and results panel
- Live weather from OpenWeatherMap API
- Current temperature (°C and °F), humidity, description, wind speed
- Weather icons fetched from OpenWeatherMap
- Hourly forecast panel: next 6 slots (3-hour steps)
- Daily forecast panel: next 5 days (min/max temps)
- °C / °F unit toggle button
- (Bonus) Auto-location detection via ipinfo.io
- All errors shown inside the GUI — no terminal prints

## Requirements

- Python 3.10+
- requests, python-dotenv, Pillow (`pip install -r requirements.txt`)
- tkinter (bundled with Python)
- A free OpenWeatherMap API key

## Setup

1. Register at https://openweathermap.org/api (free tier).
2. Copy your API key.
3. Create a `.env` file in this folder:

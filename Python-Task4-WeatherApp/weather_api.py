"""OpenWeatherMap API wrapper."""

import os
from dataclasses import dataclass
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
BASE = "https://api.openweathermap.org/data/2.5"
ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"


@dataclass
class CurrentWeather:
    temp_c: float
    temp_f: float
    humidity: int
    description: str
    wind_speed: float
    icon: str


def _check_key():
    if not API_KEY:
        raise RuntimeError(
            "OWM_API_KEY missing. Add it to the .env file."
        )


def fetch_current(city: str) -> CurrentWeather:
    _check_key()
    if not city.strip():
        raise ValueError("City cannot be empty.")

    try:
        r = requests.get(
            f"{BASE}/weather",
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
    except requests.Timeout:
        raise TimeoutError("Network timeout — please try again.")
    except requests.RequestException as e:
        raise ConnectionError(f"Network error: {e}")

    if r.status_code == 404:
        raise LookupError(f"City '{city}' not found.")
    if r.status_code == 401:
        raise PermissionError(
            "Invalid API key. Check .env, and note new keys take up to 30 min to activate."
        )
    r.raise_for_status()

    d = r.json()
    return CurrentWeather(
        temp_c=round(d["main"]["temp"], 1),
        temp_f=round(d["main"]["temp"] * 9 / 5 + 32, 1),
        humidity=d["main"]["humidity"],
        description=d["weather"][0]["description"].title(),
        wind_speed=d["wind"]["speed"],
        icon=d["weather"][0]["icon"],
    )


def fetch_hourly(city: str, slots: int = 6):
    """Return list of dicts for next `slots` 3-hour forecast entries."""
    _check_key()
    if not city.strip():
        raise ValueError("City cannot be empty.")

    try:
        r = requests.get(
            f"{BASE}/forecast",
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
    except requests.Timeout:
        raise TimeoutError("Network timeout — please try again.")
    except requests.RequestException as e:
        raise ConnectionError(f"Network error: {e}")

    if r.status_code == 404:
        raise LookupError(f"City '{city}' not found.")
    if r.status_code == 401:
        raise PermissionError("Invalid API key.")
    r.raise_for_status()

    data = r.json()["list"][:slots]
    out = []
    for item in data:
        dt = datetime.fromtimestamp(item["dt"])
        out.append({
            "time": dt.strftime("%H:%M"),
            "temp_c": round(item["main"]["temp"], 1),
            "icon": item["weather"][0]["icon"],
            "desc": item["weather"][0]["description"].title(),
        })
    return out


def fetch_daily(city: str, days: int = 5):
    """Aggregate 3-hour forecast into daily min/max."""
    _check_key()
    if not city.strip():
        raise ValueError("City cannot be empty.")

    try:
        r = requests.get(
            f"{BASE}/forecast",
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
    except requests.Timeout:
        raise TimeoutError("Network timeout — please try again.")
    except requests.RequestException as e:
        raise ConnectionError(f"Network error: {e}")

    if r.status_code == 404:
        raise LookupError(f"City '{city}' not found.")
    if r.status_code == 401:
        raise PermissionError("Invalid API key.")
    r.raise_for_status()

    buckets = {}
    for item in r.json()["list"]:
        dt = datetime.fromtimestamp(item["dt"])
        day = dt.strftime("%a %d %b")
        if day not in buckets:
            buckets[day] = {
                "temps": [],
                "icons": [],
                "descs": [],
            }
        buckets[day]["temps"].append(item["main"]["temp"])
        buckets[day]["icons"].append(item["weather"][0]["icon"])
        buckets[day]["descs"].append(item["weather"][0]["description"])

    daily = []
    for day, data in list(buckets.items())[:days]:
        daily.append({
            "day": day,
            "min_c": round(min(data["temps"]), 1),
            "max_c": round(max(data["temps"]), 1),
            "icon": data["icons"][len(data["icons"]) // 2],
            "desc": data["descs"][len(data["descs"]) // 2].title(),
        })
    return daily


def detect_location():
    """Return city name based on caller's IP (best-effort)."""
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        r.raise_for_status()
        return r.json().get("city", "")
    except Exception:
        return ""
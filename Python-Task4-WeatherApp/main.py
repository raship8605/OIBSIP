"""Weather App — Advanced tier (tkinter GUI + OpenWeatherMap)."""

import tkinter as tk
from tkinter import ttk, messagebox
from io import BytesIO

import requests
from PIL import Image, ImageTk

import weather_api as api


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App — Advanced")
        self.geometry("720x720")
        self.resizable(False, False)

        self.unit = tk.StringVar(value="C")   # C or F
        self.city_var = tk.StringVar()
        self._icon_cache = {}                 # keep PhotoImage refs alive

        self._build_ui()
        self._auto_detect_location()

    # ---------- UI ----------
    def _build_ui(self):
        pad = {"padx": 8, "pady": 6}

        top = tk.Frame(self)
        top.pack(fill="x", **pad)

        tk.Label(top, text="City:").pack(side="left")
        ttk.Entry(top, textvariable=self.city_var, width=24).pack(side="left", padx=6)
        ttk.Button(top, text="Get Weather", command=self._on_get).pack(side="left", padx=4)
        ttk.Button(top, text="°C / °F", command=self._toggle_unit).pack(side="left", padx=4)

        # Error label
        self.error_label = tk.Label(self, text="", fg="red", wraplength=680, justify="left")
        self.error_label.pack(fill="x", padx=10)

        # Current weather panel
        self.current_frame = tk.Frame(self, bd=1, relief="sunken")
        self.current_frame.pack(fill="x", padx=10, pady=8)
        self.current_icon = tk.Label(self.current_frame)
        self.current_icon.pack(side="left", padx=10, pady=10)
        info = tk.Frame(self.current_frame)
        info.pack(side="left", anchor="w", padx=10)
        self.current_temp = tk.Label(info, text="", font=("Segoe UI", 24, "bold"))
        self.current_temp.pack(anchor="w")
        self.current_desc = tk.Label(info, text="", font=("Segoe UI", 12))
        self.current_desc.pack(anchor="w")
        self.current_meta = tk.Label(info, text="", font=("Segoe UI", 10))
        self.current_meta.pack(anchor="w", pady=4)

        # Hourly forecast
        tk.Label(self, text="Next 6 hours (3-hour steps)",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10)
        self.hourly_frame = tk.Frame(self)
        self.hourly_frame.pack(fill="x", padx=10, pady=4)

        # Daily forecast
        tk.Label(self, text="Next 5 days",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        self.daily_frame = tk.Frame(self)
        self.daily_frame.pack(fill="x", padx=10, pady=4)

    # ---------- Actions ----------
    def _auto_detect_location(self):
        city = api.detect_location()
        if city:
            self.city_var.set(city)
            self._on_get()

    def _toggle_unit(self):
        self.unit.set("F" if self.unit.get() == "C" else "C")
        if self.city_var.get().strip():
            self._on_get()

    def _fmt_temp(self, temp_c, temp_f=None):
        if self.unit.get() == "C":
            return f"{temp_c}°C"
        if temp_f is not None:
            return f"{temp_f}°F"
        return f"{round(temp_c * 9 / 5 + 32, 1)}°F"

    def _on_get(self):
        city = self.city_var.get().strip()
        self.error_label.config(text="")
        self._clear_panels()

        if not city:
            self.error_label.config(text="Please enter a city name.")
            return

        try:
            current = api.fetch_current(city)
            hourly = api.fetch_hourly(city, slots=6)
            daily = api.fetch_daily(city, days=5)
        except ValueError as e:
            self.error_label.config(text=str(e))
            return
        except LookupError as e:
            self.error_label.config(text=str(e))
            return
        except PermissionError as e:
            self.error_label.config(text=str(e))
            return
        except TimeoutError as e:
            self.error_label.config(text=str(e))
            return
        except ConnectionError as e:
            self.error_label.config(text=str(e))
            return
        except Exception as e:
            self.error_label.config(text=f"Unexpected error: {e}")
            return

        # Current
        self.current_temp.config(
            text=self._fmt_temp(current.temp_c, current.temp_f)
        )
        self.current_desc.config(text=current.description)
        self.current_meta.config(
            text=f"Humidity: {current.humidity}%   •   Wind: {current.wind_speed} m/s"
        )
        self._set_icon(self.current_icon, current.icon, size=80)

        # Hourly
        for h in hourly:
            card = tk.Frame(self.hourly_frame, bd=1, relief="ridge", padx=6, pady=6)
            card.pack(side="left", padx=4)
            tk.Label(card, text=h["time"], font=("Segoe UI", 9, "bold")).pack()
            icon_lbl = tk.Label(card)
            icon_lbl.pack()
            self._set_icon(icon_lbl, h["icon"], size=40)
            tk.Label(card, text=self._fmt_temp(h["temp_c"])).pack()

        # Daily
        for d in daily:
            row = tk.Frame(self.daily_frame, bd=1, relief="ridge", padx=6, pady=6)
            row.pack(side="left", padx=4)
            tk.Label(row, text=d["day"], font=("Segoe UI", 9, "bold")).pack()
            icon_lbl = tk.Label(row)
            icon_lbl.pack()
            self._set_icon(icon_lbl, d["icon"], size=40)
            tk.Label(row, text=f"{d['max_c']} / {d['min_c']} °C").pack()

    def _clear_panels(self):
        for f in (self.hourly_frame, self.daily_frame):
            for w in f.winfo_children():
                w.destroy()
        self.current_icon.config(image="")
        self.current_temp.config(text="")
        self.current_desc.config(text="")
        self.current_meta.config(text="")

    def _set_icon(self, label, icon_code, size=64):
        try:
            key = (icon_code, size)
            if key not in self._icon_cache:
                url = api.ICON_URL.format(icon=icon_code)
                data = requests.get(url, timeout=8).content
                img = Image.open(BytesIO(data)).resize((size, size))
                self._icon_cache[key] = ImageTk.PhotoImage(img)
            label.config(image=self._icon_cache[key])
            label.image = self._icon_cache[key]  # keep reference
        except Exception:
            label.config(image="")


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
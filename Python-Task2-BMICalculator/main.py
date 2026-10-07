"""BMI Calculator — Advanced tier (tkinter GUI + SQLite + matplotlib)."""

import tkinter as tk
from tkinter import ttk, messagebox

from bmi_logic import evaluate
from database import BMIStore
from charts import build_trend_canvas


class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator — Advanced")
        self.geometry("640x680")
        self.resizable(False, False)

        self.store = BMIStore()
        self._chart_widget = None  # keep reference for refresh

        self._build_ui()
        self._refresh_users()

    # ---------- UI Construction ----------
    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        # --- User row ---
        tk.Label(self, text="User name:").grid(row=0, column=0, sticky="w", **pad)
        self.user_var = tk.StringVar()
        self.user_entry = ttk.Entry(self, textvariable=self.user_var, width=28)
        self.user_entry.grid(row=0, column=1, sticky="w", **pad)

        self.user_combo = ttk.Combobox(self, width=20, state="readonly")
        self.user_combo.grid(row=0, column=2, sticky="w", **pad)
        self.user_combo.bind("<<ComboboxSelected>>", self._on_user_selected)

        # --- Weight ---
        tk.Label(self, text="Weight (kg):").grid(row=1, column=0, sticky="w", **pad)
        self.weight_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.weight_var, width=28).grid(
            row=1, column=1, sticky="w", **pad
        )

        # --- Height ---
        tk.Label(self, text="Height (m or cm):").grid(row=2, column=0, sticky="w", **pad)        
        self.height_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.height_var, width=28).grid(
            row=2, column=1, sticky="w", **pad
        )

        # --- Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Calculate & Save", command=self._calculate).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Clear", command=self._clear).pack(
            side="left", padx=5
        )

        # --- Result ---
        self.result_label = tk.Label(
            self, text="", font=("Segoe UI", 14, "bold")
        )
        self.result_label.grid(row=4, column=0, columnspan=3, pady=8)

        # --- Chart frame ---
        self.chart_frame = tk.Frame(self, bd=1, relief="sunken")
        self.chart_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10,
                              sticky="nsew")

    # ---------- Handlers ----------
    def _refresh_users(self):
        try:
            users = self.store.list_users()
        except RuntimeError as e:
            messagebox.showerror("Database error", str(e))
            users = []
        self.user_combo["values"] = users

    def _on_user_selected(self, _event):
        self.user_var.set(self.user_combo.get())
        self._load_chart()

    def _parse_inputs(self):
        user = self.user_var.get().strip()
        if not user:
            raise ValueError("Please enter a user name.")

        try:
            weight = float(self.weight_var.get())
        except ValueError:
            raise ValueError("Weight must be a number.")

        try:
            height = float(self.height_var.get())
        except ValueError:
            raise ValueError("Height must be a number.")

        return user, weight, height

    def _calculate(self):
        try:
            user, weight, height = self._parse_inputs()
            result = evaluate(weight, height)
            self.store.add_record(user, weight, height,
                                  result.bmi, result.category)
        except ValueError as e:
            messagebox.showwarning("Invalid input", str(e))
            return
        except RuntimeError as e:
            messagebox.showerror("Database error", str(e))
            return

        self.result_label.config(
            text=f"BMI: {result.bmi}  —  {result.category}",
            fg=result.color,
        )
        self._refresh_users()
        self.user_combo.set(user)
        self._load_chart()

    def _clear(self):
        self.weight_var.set("")
        self.height_var.set("")
        self.result_label.config(text="")

    def _load_chart(self):
        user = self.user_var.get().strip()
        if self._chart_widget is not None:
            self._chart_widget.destroy()

        if not user:
            history = []
        else:
            try:
                history = self.store.get_history(user)
            except RuntimeError as e:
                messagebox.showerror("Database error", str(e))
                history = []

        self._chart_widget = build_trend_canvas(self.chart_frame, history)
        self._chart_widget.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
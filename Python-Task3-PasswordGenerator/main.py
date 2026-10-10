"""Password Generator — Advanced tier (tkinter + secrets + pyperclip)."""

import tkinter as tk
from tkinter import ttk, messagebox

import pyperclip

from generator import build_pools, generate_password, strength_label


class PasswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator — Advanced")
        self.geometry("540x560")
        self.resizable(False, False)

        self.history = []   # last 5 passwords (session only)

        # Vars
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.ambig_var = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar()
        self.strength_var = tk.StringVar(value="")

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        # Length slider
        tk.Label(self, text="Password length:").grid(row=0, column=0, sticky="w", **pad)
        self.length_label = tk.Label(self, text="16", width=3)
        self.length_label.grid(row=0, column=2, sticky="w", **pad)
        scale = ttk.Scale(
            self, from_=8, to=64, orient="horizontal",
            variable=self.length_var, length=280,
            command=self._on_length_change,
        )
        scale.grid(row=0, column=1, sticky="w", **pad)

        # Character types
        tk.Label(self, text="Character types:").grid(row=1, column=0, sticky="nw", **pad)
        types_frame = tk.Frame(self)
        types_frame.grid(row=1, column=1, columnspan=2, sticky="w", **pad)
        ttk.Checkbutton(types_frame, text="Uppercase (A-Z)",
                        variable=self.upper_var).pack(anchor="w")
        ttk.Checkbutton(types_frame, text="Lowercase (a-z)",
                        variable=self.lower_var).pack(anchor="w")
        ttk.Checkbutton(types_frame, text="Digits (0-9)",
                        variable=self.digits_var).pack(anchor="w")
        ttk.Checkbutton(types_frame, text="Symbols (!@#$...)",
                        variable=self.symbols_var).pack(anchor="w")

        # Ambiguous toggle
        ttk.Checkbutton(self, text="Exclude ambiguous characters (0 O l 1 I)",
                        variable=self.ambig_var).grid(
            row=2, column=0, columnspan=3, sticky="w", **pad
        )

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Generate", command=self._generate).pack(
            side="left", padx=6
        )
        ttk.Button(btn_frame, text="Copy to Clipboard", command=self._copy).pack(
            side="left", padx=6
        )

        # Output
        tk.Label(self, text="Generated password:").grid(
            row=4, column=0, columnspan=3, sticky="w", **pad
        )
        entry = ttk.Entry(self, textvariable=self.password_var,
                          font=("Consolas", 12), width=44)
        entry.grid(row=5, column=0, columnspan=3, sticky="we", **pad)

        # Strength
        self.strength_label = tk.Label(self, text="", font=("Segoe UI", 12, "bold"))
        self.strength_label.grid(row=6, column=0, columnspan=3, pady=4)

        # History
        tk.Label(self, text="Session history (last 5):").grid(
            row=7, column=0, columnspan=3, sticky="w", **pad
        )
        self.history_box = tk.Listbox(self, height=5, font=("Consolas", 10))
        self.history_box.grid(row=8, column=0, columnspan=3, sticky="we", **pad)

    # ---------- Handlers ----------
    def _on_length_change(self, _value):
        self.length_label.config(text=str(self.length_var.get()))

    def _current_pools(self):
        return build_pools(
            self.upper_var.get(),
            self.lower_var.get(),
            self.digits_var.get(),
            self.symbols_var.get(),
            self.ambig_var.get(),
        )

    def _generate(self):
        pools = self._current_pools()
        try:
            pwd = generate_password(self.length_var.get(), pools)
        except ValueError as e:
            messagebox.showwarning("Invalid settings", str(e))
            return

        self.password_var.set(pwd)

        # Strength
        label, color = strength_label(self.length_var.get(), len(pools))
        self.strength_label.config(text=f"Strength: {label}", fg=color)

        # Auto-copy
        try:
            pyperclip.copy(pwd)
            self.title("Password Generator — Advanced  ✓ Copied")
            self.after(1500, lambda: self.title("Password Generator — Advanced"))
        except Exception as e:
            messagebox.showwarning("Clipboard error", str(e))

        # Session history
        self.history.insert(0, pwd)
        self.history = self.history[:5]
        self._refresh_history_box()

    def _refresh_history_box(self):
        self.history_box.delete(0, tk.END)
        for pwd in self.history:
            self.history_box.insert(tk.END, pwd)

    def _copy(self):
        pwd = self.password_var.get()
        if not pwd:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        try:
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Clipboard error", str(e))


if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()
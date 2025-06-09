import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class OnboardingTab:
    def __init__(self, notebook):
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="👤 Onboarding")

        self.entries = {}
        for i, field in enumerate(["Name", "Email", "Abteilung", "Startdatum"]):
            tk.Label(self.tab, text=field).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(self.tab, width=30)
            entry.grid(row=i, column=1, pady=2)
            self.entries[field] = entry

        tk.Button(self.tab, text="Speichern", command=self.save_data).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self.tab, text="Anzeigen", command=self.show_data).grid(row=6, column=0, columnspan=2, pady=5)

        self.output = tk.Text(self.tab, height=10)
        self.output.grid(row=7, column=0, columnspan=2, sticky="nsew")

        self.tab.grid_rowconfigure(7, weight=1)
        self.tab.grid_columnconfigure(1, weight=1)

        self.filename = "onboarding_daten.json"

    def save_data(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Fehler", "Alle Felder ausfüllen!")
            return
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                all_data = json.load(f)
        else:
            all_data = []
        all_data.append(data)
        with open(self.filename, "w") as f:
            json.dump(all_data, f, indent=4)
        messagebox.showinfo("Gespeichert", "Mitarbeiterdaten gespeichert.")

    def show_data(self):
        self.output.delete("1.0", tk.END)
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                all_data = json.load(f)
                for person in all_data:
                    self.output.insert(tk.END, json.dumps(person, indent=2) + "\n")
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import os

class BackupTab:
    def __init__(self, notebook):
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="💾 Backup Tool")

        tk.Button(self.tab, text="Dateien wählen", command=self.select_files).pack(pady=5)
        tk.Button(self.tab, text="Zielordner wählen", command=self.select_backup_dir).pack(pady=5)
        tk.Button(self.tab, text="Backup starten", command=self.perform_backup).pack(pady=5)

        self.backup_log = tk.Text(self.tab, height=10)
        self.backup_log.pack(fill="both", expand=True)

        self.files = []
        self.target_dir = ""

    def select_files(self):
        self.files = filedialog.askopenfilenames(title="Dateien wählen")

    def select_backup_dir(self):
        self.target_dir = filedialog.askdirectory(title="Zielordner wählen")

    def perform_backup(self):
        if not self.files or not self.target_dir:
            messagebox.showwarning("Fehler", "Dateien und Zielordner müssen gewählt werden!")
            return
        for file in self.files:
            try:
                shutil.copy(file, self.target_dir)
                self.backup_log.insert(tk.END, f"✔ Backup: {os.path.basename(file)}\n")
            except Exception as e:
                self.backup_log.insert(tk.END, f"❌ Fehler bei {file}: {str(e)}\n")
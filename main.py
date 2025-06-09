import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import json
import os
import fitz  # PyMuPDF

class MultiToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Firmen-Tools")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.create_pdf_viewer_tab()
        self.create_backup_tab()
        self.create_onboarding_tab()

    # ---------- PDF Viewer ----------
    def create_pdf_viewer_tab(self):
        self.pdf_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.pdf_tab, text="📄 PDF Viewer")

        self.pdf_text = tk.Text(self.pdf_tab, wrap="word", height=30, width=80)
        self.pdf_text.pack()

        self.pdf_controls = tk.Frame(self.pdf_tab)
        self.pdf_controls.pack()

        tk.Button(self.pdf_controls, text="PDF laden", command=self.load_pdf).pack(side=tk.LEFT)
        tk.Button(self.pdf_controls, text="◀️", command=self.prev_page).pack(side=tk.LEFT)
        tk.Button(self.pdf_controls, text="▶️", command=self.next_page).pack(side=tk.LEFT)

        self.pdf_doc = None
        self.pdf_page_number = 0

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Dateien", "*.pdf")])
        if file_path:
            self.pdf_doc = fitz.open(file_path)
            self.pdf_page_number = 0
            self.show_pdf_page()

    def show_pdf_page(self):
        if self.pdf_doc:
            page = self.pdf_doc.load_page(self.pdf_page_number)
            text = page.get_text()
            self.pdf_text.delete("1.0", tk.END)
            self.pdf_text.insert(tk.END, text)

    def prev_page(self):
        if self.pdf_doc and self.pdf_page_number > 0:
            self.pdf_page_number -= 1
            self.show_pdf_page()

    def next_page(self):
        if self.pdf_doc and self.pdf_page_number < len(self.pdf_doc) - 1:
            self.pdf_page_number += 1
            self.show_pdf_page()

    # ---------- Backup Tool ----------
    def create_backup_tab(self):
        self.backup_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.backup_tab, text="💾 Backup Tool")

        tk.Button(self.backup_tab, text="Dateien wählen", command=self.select_files).pack(pady=5)
        tk.Button(self.backup_tab, text="Zielordner wählen", command=self.select_backup_dir).pack(pady=5)
        tk.Button(self.backup_tab, text="Backup starten", command=self.perform_backup).pack(pady=5)

        self.backup_files = []
        self.backup_dir = ""
        self.backup_log = tk.Text(self.backup_tab, height=10)
        self.backup_log.pack(fill="x")

    def select_files(self):
        self.backup_files = filedialog.askopenfilenames(title="Dateien wählen")

    def select_backup_dir(self):
        self.backup_dir = filedialog.askdirectory(title="Zielordner wählen")

    def perform_backup(self):
        if not self.backup_files or not self.backup_dir:
            messagebox.showwarning("Fehler", "Dateien und Zielordner müssen gewählt werden!")
            return
        for file in self.backup_files:
            try:
                shutil.copy(file, self.backup_dir)
                self.backup_log.insert(tk.END, f"Backup erfolgreich: {os.path.basename(file)}\n")
            except Exception as e:
                self.backup_log.insert(tk.END, f"Fehler bei {file}: {str(e)}\n")

    # ---------- Onboarding ----------
    def create_onboarding_tab(self):
        self.onboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.onboard_tab, text="👤 Onboarding")

        self.entries = {}
        for idx, field in enumerate(["Name", "Email", "Abteilung", "Startdatum"]):
            tk.Label(self.onboard_tab, text=field).grid(row=idx, column=0, sticky="e")
            entry = tk.Entry(self.onboard_tab, width=30)
            entry.grid(row=idx, column=1)
            self.entries[field] = entry

        tk.Button(self.onboard_tab, text="Speichern", command=self.save_onboarding_data).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self.onboard_tab, text="Anzeigen", command=self.show_onboarding_data).grid(row=6, column=0, columnspan=2, pady=5)

        self.onboard_output = tk.Text(self.onboard_tab, height=10)
        self.onboard_output.grid(row=7, column=0, columnspan=2)

        self.onboarding_file = "onboarding_daten.json"

    def save_onboarding_data(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen!")
            return
        if os.path.exists(self.onboarding_file):
            with open(self.onboarding_file, "r") as f:
                all_data = json.load(f)
        else:
            all_data = []
        all_data.append(data)
        with open(self.onboarding_file, "w") as f:
            json.dump(all_data, f, indent=4)
        messagebox.showinfo("Gespeichert", "Daten wurden gespeichert.")

    def show_onboarding_data(self):
        self.onboard_output.delete("1.0", tk.END)
        if os.path.exists(self.onboarding_file):
            with open(self.onboarding_file, "r") as f:
                data = json.load(f)
                for person in data:
                    self.onboard_output.insert(tk.END, json.dumps(person, indent=2) + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiToolApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox, filedialog
from model.haushaltsbuch_model import HaushaltsbuchModel
from view.haushaltsbuch_view import HaushaltsbuchView

class HaushaltsbuchController:
    def __init__(self, root):
        self.model = HaushaltsbuchModel()
        self.view = HaushaltsbuchView(root)
        self.register_events()
        self.update_uebersicht()
        self.update_listbox()

    def register_events(self):
        self.view.einnahme_btn.config(command=lambda: self.eintrag_hinzufuegen("Einnahme"))
        self.view.ausgabe_btn.config(command=lambda: self.eintrag_hinzufuegen("Ausgabe"))
        self.view.speichern_btn.config(command=self.speichern)
        self.view.laden_btn.config(command=self.laden)
        self.view.diagramm_btn.config(command=self.zeige_diagramm)

    def eintrag_hinzufuegen(self, typ):
        betrag_str = self.view.betrag_entry.get()
        beschreibung = self.view.beschreibung_entry.get()
        kategorie = self.view.kategorie_var.get()
        try:
            betrag = float(betrag_str)
            if betrag <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Fehler", "Bitte einen positiven Zahlenwert für den Betrag eingeben!")
            return
        if not beschreibung:
            messagebox.showwarning("Fehler", "Bitte eine Beschreibung eingeben!")
            return
        self.model.eintrag_hinzufuegen(typ, betrag, beschreibung, kategorie)
        self.view.betrag_entry.delete(0, 'end')
        self.view.beschreibung_entry.delete(0, 'end')
        self.update_uebersicht()
        self.update_listbox()

    def update_uebersicht(self):
        gesamt_einnahmen, gesamt_ausgaben, saldo = self.model.get_uebersicht()
        text = f"Gesamteinnahmen: {gesamt_einnahmen:.2f} € | Gesamtausgaben: {gesamt_ausgaben:.2f} € | Saldo: {saldo:.2f} €"
        self.view.uebersicht_label.config(text=text)
        if saldo < 0:
            messagebox.showwarning("Achtung", "Achtung: Budget überschritten!")

    def update_listbox(self):
        self.view.listbox.delete(0, 'end')
        for typ, betrag, beschreibung, kategorie in self.model.get_eintraege():
            self.view.listbox.insert('end', f"{typ}: {betrag:.2f} € - {beschreibung} [{kategorie}]")

    def speichern(self):
        pfad = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Textdateien", "*.txt")])
        if not pfad:
            return
        try:
            self.model.speichern(pfad)
            messagebox.showinfo("Gespeichert", "Einträge wurden gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")

    def laden(self):
        pfad = filedialog.askopenfilename(filetypes=[("Textdateien", "*.txt")])
        if not pfad:
            return
        try:
            self.model.laden(pfad)
            self.update_uebersicht()
            self.update_listbox()
            messagebox.showinfo("Geladen", "Einträge wurden geladen.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden: {e}")

    def zeige_diagramm(self):
        win = self.view.root = self.view.root
        diagramm_win = tk.Toplevel(win)
        diagramm_win.title("Diagramm Einnahmen vs. Ausgaben")
        diagramm_win.geometry("500x250")
        diagramm_win.resizable(False, False)
        canvas = tk.Canvas(diagramm_win, width=500, height=250)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def draw_diagram():
            canvas.delete("all")
            width = 500
            height = 250
            margin = 50
            bar_height = 40
            spacing = 30
            text_margin = 10
            einnahmen, ausgaben, _ = self.model.get_uebersicht()
            max_betrag = max(einnahmen, ausgaben, 1)
            max_bar_width = width - 2 * margin - 80
            einnahmen_balken = int((einnahmen / max_betrag) * max_bar_width)
            ausgaben_balken = int((ausgaben / max_betrag) * max_bar_width)
            # Einnahmen (grün)
            y1 = margin
            y2 = y1 + bar_height
            canvas.create_rectangle(margin, y1, margin + einnahmen_balken, y2, fill="green")
            einnahmen_text = f"Einnahmen: {einnahmen:.2f} €"
            canvas.create_text(margin, y2 + 15, text=einnahmen_text, anchor="w", fill="black")
            # Ausgaben (rot)
            y1 = y2 + spacing
            y2 = y1 + bar_height
            canvas.create_rectangle(margin, y1, margin + ausgaben_balken, y2, fill="red")
            ausgaben_text = f"Ausgaben: {ausgaben:.2f} €"
            canvas.create_text(margin, y2 + 15, text=ausgaben_text, anchor="w", fill="black")

        draw_diagram() 
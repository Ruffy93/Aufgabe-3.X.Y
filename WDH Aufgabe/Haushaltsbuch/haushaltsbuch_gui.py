import tkinter as tk
from tkinter import messagebox, filedialog
from haushaltsbuch_model import HaushaltsbuchModel

KATEGORIEN = ["Allgemein", "Essen", "Freizeit", "Fixkosten", "Sonstiges"]

class HaushaltsbuchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Haushaltsbuch")
        self.model = HaushaltsbuchModel()

        # Eingabefelder
        tk.Label(root, text="Betrag:").grid(row=0, column=0, sticky="e")
        self.betrag_entry = tk.Entry(root)
        self.betrag_entry.grid(row=0, column=1)

        tk.Label(root, text="Beschreibung:").grid(row=1, column=0, sticky="e")
        self.beschreibung_entry = tk.Entry(root)
        self.beschreibung_entry.grid(row=1, column=1)

        tk.Label(root, text="Kategorie:").grid(row=2, column=0, sticky="e")
        self.kategorie_var = tk.StringVar(value=KATEGORIEN[0])
        self.kategorie_menu = tk.OptionMenu(root, self.kategorie_var, *KATEGORIEN)
        self.kategorie_menu.grid(row=2, column=1, sticky="w")

        # Buttons
        tk.Button(root, text="Einnahme hinzufügen", command=self.einnahme_hinzufuegen).grid(row=3, column=0, pady=5)
        tk.Button(root, text="Ausgabe hinzufügen", command=self.ausgabe_hinzufuegen).grid(row=3, column=1, pady=5)
        tk.Button(root, text="Speichern", command=self.speichern).grid(row=4, column=0, pady=5)
        tk.Button(root, text="Laden", command=self.laden).grid(row=4, column=1, pady=5)
        tk.Button(root, text="Diagramm anzeigen", command=self.zeige_diagramm).grid(row=5, column=0, columnspan=2, pady=5)

        # Übersicht
        self.uebersicht_label = tk.Label(root, text="Gesamteinnahmen: 0.00 € | Gesamtausgaben: 0.00 € | Saldo: 0.00 €")
        self.uebersicht_label.grid(row=6, column=0, columnspan=2, pady=5)

        # Listbox für Einträge
        self.listbox = tk.Listbox(root, width=60)
        self.listbox.grid(row=7, column=0, columnspan=2, pady=5)

    def einnahme_hinzufuegen(self):
        self.eintrag_hinzufuegen("Einnahme")

    def ausgabe_hinzufuegen(self):
        self.eintrag_hinzufuegen("Ausgabe")

    def eintrag_hinzufuegen(self, typ):
        betrag_str = self.betrag_entry.get()
        beschreibung = self.beschreibung_entry.get()
        kategorie = self.kategorie_var.get()
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
        self.betrag_entry.delete(0, tk.END)
        self.beschreibung_entry.delete(0, tk.END)
        self.update_uebersicht()
        self.update_listbox()

    def update_uebersicht(self):
        gesamt_einnahmen, gesamt_ausgaben, saldo = self.model.get_uebersicht()
        text = f"Gesamteinnahmen: {gesamt_einnahmen:.2f} € | Gesamtausgaben: {gesamt_ausgaben:.2f} € | Saldo: {saldo:.2f} €"
        self.uebersicht_label.config(text=text)
        if saldo < 0:
            messagebox.showwarning("Achtung", "Achtung: Budget überschritten!")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for typ, betrag, beschreibung, kategorie in self.model.get_eintraege():
            self.listbox.insert(tk.END, f"{typ}: {betrag:.2f} € - {beschreibung} [{kategorie}]")

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
        win = tk.Toplevel(self.root)
        win.title("Diagramm Einnahmen vs. Ausgaben")
        win.geometry("500x250")
        win.resizable(False, False)
        canvas = tk.Canvas(win, width=500, height=250)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def draw_diagram(event=None):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = HaushaltsbuchGUI(root)
    root.mainloop() 
import tkinter as tk

KATEGORIEN = ["Allgemein", "Essen", "Freizeit", "Fixkosten", "Sonstiges"]

class HaushaltsbuchView:
    def __init__(self, root):
        self.root = root
        self.root.title("Haushaltsbuch")

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
        self.einnahme_btn = tk.Button(root, text="Einnahme hinzufügen")
        self.einnahme_btn.grid(row=3, column=0, pady=5)
        self.ausgabe_btn = tk.Button(root, text="Ausgabe hinzufügen")
        self.ausgabe_btn.grid(row=3, column=1, pady=5)
        self.speichern_btn = tk.Button(root, text="Speichern")
        self.speichern_btn.grid(row=4, column=0, pady=5)
        self.laden_btn = tk.Button(root, text="Laden")
        self.laden_btn.grid(row=4, column=1, pady=5)
        self.diagramm_btn = tk.Button(root, text="Diagramm anzeigen")
        self.diagramm_btn.grid(row=5, column=0, columnspan=2, pady=5)

        # Übersicht
        self.uebersicht_label = tk.Label(root, text="Gesamteinnahmen: 0.00 € | Gesamtausgaben: 0.00 € | Saldo: 0.00 €")
        self.uebersicht_label.grid(row=6, column=0, columnspan=2, pady=5)

        # Listbox für Einträge
        self.listbox = tk.Listbox(root, width=60)
        self.listbox.grid(row=7, column=0, columnspan=2, pady=5) 
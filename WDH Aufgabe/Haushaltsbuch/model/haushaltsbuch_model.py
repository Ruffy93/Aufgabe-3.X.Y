import os

class HaushaltsbuchModel:
    def __init__(self):
        self.einnahmen = []
        self.ausgaben = []
        self.eintraege = []  # (Typ, Betrag, Beschreibung, Kategorie)

    def eintrag_hinzufuegen(self, typ, betrag, beschreibung, kategorie):
        if typ == "Einnahme":
            self.einnahmen.append(betrag)
        else:
            self.ausgaben.append(betrag)
        self.eintraege.append((typ, betrag, beschreibung, kategorie))

    def get_uebersicht(self):
        gesamt_einnahmen = sum(self.einnahmen)
        gesamt_ausgaben = sum(self.ausgaben)
        saldo = gesamt_einnahmen - gesamt_ausgaben
        return gesamt_einnahmen, gesamt_ausgaben, saldo

    def get_eintraege(self):
        return list(self.eintraege)

    def speichern(self, pfad):
        with open(pfad, "w", encoding="utf-8") as f:
            for typ, betrag, beschreibung, kategorie in self.eintraege:
                f.write(f"{typ};{betrag};{beschreibung};{kategorie}\n")

    def laden(self, pfad):
        if not os.path.exists(pfad):
            return
        self.einnahmen.clear()
        self.ausgaben.clear()
        self.eintraege.clear()
        with open(pfad, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 4:
                    typ, betrag, beschreibung, kategorie = parts
                    betrag = float(betrag)
                    if typ == "Einnahme":
                        self.einnahmen.append(betrag)
                    else:
                        self.ausgaben.append(betrag)
                    self.eintraege.append((typ, betrag, beschreibung, kategorie)) 
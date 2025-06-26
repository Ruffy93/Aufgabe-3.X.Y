def einnahme_hinzufuegen(einnahmen):
    while True:
        try:
            betrag = float(input("Einnahme-Betrag: "))
            if betrag <= 0:
                print("Nur positive Zahlen erlaubt!")
                continue
            einnahmen.append(betrag)
            break
        except ValueError:
            print("Ungültige Eingabe. Bitte Zahl eingeben.")

def ausgabe_hinzufuegen(ausgaben):
    while True:
        try:
            betrag = float(input("Ausgabe-Betrag: "))
            if betrag <= 0:
                print("Nur positive Zahlen erlaubt!")
                continue
            ausgaben.append(betrag)
            break
        except ValueError:
            print("Ungültige Eingabe. Bitte Zahl eingeben.")

def zeige_uebersicht(einnahmen, ausgaben):
    gesamt_einnahmen = sum(einnahmen)
    gesamt_ausgaben = sum(ausgaben)
    saldo = gesamt_einnahmen - gesamt_ausgaben
    print(f"Gesamteinnahmen: {gesamt_einnahmen:.2f} €")
    print(f"Gesamtausgaben: {gesamt_ausgaben:.2f} €")
    print(f"Saldo: {saldo:.2f} €")
    if saldo < 0:
        print("Achtung: Budget überschritten!")

def main():
    einnahmen = []
    ausgaben = []
    while True:
        print("\nMenü:")
        print("1. Einnahme hinzufügen")
        print("2. Ausgabe hinzufügen")
        print("3. Übersicht anzeigen")
        print("4. Beenden")
        wahl = input("Auswahl: ")
        if wahl == "1":
            einnahme_hinzufuegen(einnahmen)
        elif wahl == "2":
            ausgabe_hinzufuegen(ausgaben)
        elif wahl == "3":
            zeige_uebersicht(einnahmen, ausgaben)
        elif wahl == "4":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
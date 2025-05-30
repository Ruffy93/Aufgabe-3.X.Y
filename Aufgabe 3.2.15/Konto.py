class BankAccount:
    def __init__(self, kontoinhaber, ueberziehungsrahmen=-2000.0, gebuehr_prozent=13.73):
        self.kontoinhaber = kontoinhaber
        self.kontostand = 0.0
        self.ueberziehungsrahmen = ueberziehungsrahmen
        self.gebuehr_prozent = gebuehr_prozent

    def einzahlen(self, betrag):
        if betrag > 0.01:
            self.kontostand += betrag
            print(f"{betrag:.2f} € eingezahlt.")
        else:
            print("Kleinster möglicher Einzahlungsbetrag: 0,01€.")

    def abheben(self, betrag):
        if betrag <= 0.01:
            print("Kleinster möglicher Abhebungsbetrag: 0,01€.")
            return

        neuer_stand = self.kontostand - betrag

        if neuer_stand >= self.ueberziehungsrahmen:
            vorher_war_positiv = self.kontostand >= 0
            self.kontostand = neuer_stand
            print(f"{betrag:.2f} € abgehoben.")

            if vorher_war_positiv and self.kontostand < 0:
                gebuehr = abs(self.kontostand) * (self.gebuehr_prozent / 100)
                self.kontostand -= gebuehr
                print(f"Überziehungsgebühr von {gebuehr:.2f} € ({self.gebuehr_prozent:.1f}%) erhoben.")
        else:
            print("Abhebung abgelehnt: Überziehungslimit überschritten!")

    def zeige_kontostand(self):
        print(f"Aktueller Kontostand: {self.kontostand:.2f} €")

    def zinsen_berechnen(self, zinssatz):
        if self.kontostand > 0:
            zinsen = self.kontostand * (zinssatz / 100)
            self.kontostand += zinsen
            print(f"Zinsen in Höhe von {zinsen:.2f} € gutgeschrieben.")
        else:
            print("Keine Zinsen auf Dispo oder leere Kontostände.")

    def __str__(self):
        return f"Konto von {self.kontoinhaber} – Kontostand: {self.kontostand:.2f} €"
    

konto = BankAccount("Rafael Neumann")
print(konto)

konto.einzahlen(150.00)
konto.abheben(700.00)
konto.zeige_kontostand()
konto.zinsen_berechnen(3.45)
print(konto)
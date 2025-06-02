from Konto import BankKonto

konto = BankKonto ("Rafael Neumann")
print(konto)

konto.einzahlen(150.00)
konto.abheben(700.00)
konto.zeige_kontostand()
konto.zinsen_berechnen(3.45)
print(konto) 
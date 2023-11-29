#!/usr/bin/env python3

from forex_python.converter import CurrencyRates
import json
import os

class CurrencyConverter:

    def __init__(self):
        self.currency_rates = CurrencyRates()
        self.history_file = 'conversion_history.json'
        self.load_conversion_history()

    def load_conversion_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                self.conversion_history = json.load(file)
        else:
            self.conversion_history = []

    def save_conversion_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.conversion_history, file, indent=2)

    def convert_currency(self, amount, from_currency, to_currency):
        try:
            amount = float(input("Entrez le montant à convertir : "))
        except ValueError:
            print("Veuillez entrer un montant valide.")
            return

        try:
            rate = self.currency_rates.get_rate(from_currency, to_currency)
            converted_amount = round(amount * rate, 2)
            conversion_result = f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"

            self.conversion_history.append({
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "converted_amount": converted_amount
            })

            self.save_conversion_history()

            print(conversion_result)

        except forex_python.converter.RatesNotAvailableError:
            print("La conversion est impossible. Vérifiez les devises fournies.")

    def add_custom_currency(self, currency, rate):
        self.currency_rates.add_rate('USD', currency, rate)

    def get_user_preferences(self):
        preferred_currencies = []
        while True:
            currency = input("Entrez une devise préférée (ou tapez 'q' pour terminer) : ").upper()
            if currency == 'Q':
                break

            try:
                rate = float(input(f"Entrez le taux de conversion de {currency} par rapport au dollar : "))
                preferred_currencies.append((currency, rate))
            except ValueError:
                print("Veuillez entrer un taux de conversion valide.")

        return preferred_currencies

    def display_menu(self):
        print("\n1. Convertir une devise")
        print("2. Afficher l'historique des conversions")
        print("3. Quitter")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choisissez une option : ")

            if choice == '1':
                from_currency = input("Entrez la devise d'origine : ").upper()
                to_currency = input("Entrez la devise cible : ").upper()

                self.convert_currency(0, from_currency, to_currency)

            elif choice == '2':
                print("Historique des conversions :")
                for entry in self.conversion_history:
                    print(f"{entry['amount']} {entry['from_currency']} = {entry['converted_amount']} {entry['to_currency']}")

            elif choice == '3':
                print("Merci d'avoir utilisé le convertisseur de devises. Au revoir!")
                break

            else:
                print("Choix invalide. Veuillez entrer un nombre de 1 à 3.")

if __name__ == "__main__":
    converter = CurrencyConverter()
    converter.run()
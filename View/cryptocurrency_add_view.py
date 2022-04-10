from tkinter import ttk
import tkinter as tk
import numpy as np


class CryptocurrencyAddView:

    def __init__(self, controller: 'ProfitechController'):

        self.controller = controller
        self.frame = ""

    def afficher(self, coins):

        self.frame = ttk.Frame(self.controller.window, padding=10)
        self.frame.grid()

        label = ttk.Label(self.frame, text="Sélectionnez la cryptomonnaie à ajouter :")
        label.grid(column=0, row=0)

        # Il faut transformer le tableau de 2 à 1 dimension. Combobox transforme le format
        # d'un tableau à 2 dimensions en Tcl et modifie certains caractères (en ajoutant "{}"
        # par exemple)
        coins_values = []
        for coin in coins:
            coins_values.append(coin[1] + " " + coin[2])

        crypto_choose = ttk.Combobox(self.frame, state="readonly", values=coins_values)
        crypto_choose.grid(column=0, row=1)
        crypto_choose.current(0)

        var_success_message = tk.StringVar()

        label_success_message = ttk.Label(self.frame, textvariable=var_success_message)
        label_success_message.grid(column=0, row=2)

        ttk.Button(self.frame, text="Ajouter", command=lambda: self.controller.add_cryptocurrencies_historical_data(crypto_choose.get(), coins, var_success_message, crypto_choose)).grid(column=0, row=3)



    def close(self):
        self.frame.destroy()



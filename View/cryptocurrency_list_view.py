from tkinter import *
from tkinter import ttk


class CryptocurrencyListView:

    def __init__(self, controller: 'ProfitechController'):

        self.controller = controller
        self.frame = ""

    def afficher(self):

        self.frame = ttk.Frame(self.controller.window, padding=10)
        self.frame.grid()

        ttk.Button(self.frame, text="Ajouter une cryptomonnaie", command=lambda: self.controller.switch_frame(self, self.controller.cryptocurrency_add, args=self.controller.get_cryptocurrencies_not_uses())).grid(column=0, row=0)

        cryptocurrencies = self.controller.get_cryptocurrencies_uses()
        rows = len(cryptocurrencies)
        columns = len(cryptocurrencies[0])
        frame_table = ttk.Frame(self.frame, padding=10)
        frame_table.grid()

        ttk.Label(frame_table, text="Identifiant").grid(column=0, row=1)
        ttk.Label(frame_table, text="Symbole").grid(column=1, row=1)
        ttk.Label(frame_table, text="Nom").grid(column=2, row=1)
        ttk.Label(frame_table, text="Rang").grid(column=3, row=1)
        ttk.Label(frame_table, text="").grid(column=4, row=1)

        for row in range(rows):
            for column in range(columns):
                entry = ttk.Entry(frame_table, width=12)
                entry.grid(column=column, row=row + 2)
                entry.insert(END, cryptocurrencies[row][column])
                entry.config(state='readonly')
            ttk.Button(frame_table, text="Supprimer", command=lambda crypto_id=cryptocurrencies[row][0]: self.controller.delete_historical_data_crypto(crypto_id)).grid(column=4, row=row + 2)

    def close(self):
        self.frame.destroy()



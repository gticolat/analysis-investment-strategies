import numpy as np
import time
from tkinter import *

from Class.auth import Auth
from Class.coin_data import CoinData

from View.auth_view import AuthView
from View.home_view import HomeView
from View.cryptocurrency_list_view import CryptocurrencyListView
from View.cryptocurrency_add_view import CryptocurrencyAddView

from Model.user_model import UserModel
from Model.cryptocurrency_model import CryptocurrencyModel
from Model.historical_data_model import HistoricalDataModel


class ProfitechController:

    def __init__(self):

        # Instanciation des modèles
        self.user_model = UserModel()
        self.cryptocurrency_model = CryptocurrencyModel()
        self.historical_data_model = HistoricalDataModel()

        # Instanciation des classes de traitements
        self.auth = Auth(self.user_model)
        self.coin_data = CoinData()

        # Création de la fenêtre
        self.window = Tk()

        self.window.title("Profitech Analysis")
        self.window.geometry("720x480")
        self.window.minsize(480, 360)
        self.window.iconbitmap("View/asset/image/logo.ico")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        # Instanciation des vues
        self.auth_view = AuthView(self)
        self.home_view = HomeView(self)
        self.cryptocurrency_list = CryptocurrencyListView(self)
        self.cryptocurrency_add = CryptocurrencyAddView(self)

        # Lancement de la première vue
        self.auth_view.afficher()
        self.window.mainloop()

        self.id_user = -1

    def first_launch(self):
        major_coins = self.coin_data.get_major_coins()

        self.cryptocurrency_model.insert(major_coins)

    def switch_frame(self, old_frame, new_frame, args=None):
        old_frame.close()
        if args is not None:
            new_frame.afficher(args)
        else:
            new_frame.afficher()
        self.window.update_idletasks()

    def auth_user(self, pseudo, password, var_message_error):
        user = self.user_model.select_user(pseudo)
        auth_result = self.auth.auth_user(user, pseudo, password)

        if auth_result == -1:
            var_message_error.set("Veuillez renseigner les champs.")
        elif auth_result == 0:
            var_message_error.set("Le pseudo ou le mot de passe est incorrect.")
        elif auth_result == 1:
            self.id_user = user[0]
            self.switch_frame(self.auth_view, self.home_view)

    def get_cryptocurrencies_uses(self):
        cryptocurrencies = self.cryptocurrency_model.select_uses()

        return cryptocurrencies

    def get_cryptocurrencies_not_uses(self):
        crypto_uses = self.get_cryptocurrencies_uses()
        major_crypto = self.cryptocurrency_model.select_all()
        crypto_not_uses = []

        for crypto in major_crypto:
            if crypto not in crypto_uses:
                crypto_not_uses.append(crypto)

        return crypto_not_uses

    def add_cryptocurrencies_historical_data(self, coin_choose, all_coins, var_success_message, combobox):
        split_coin_choose = coin_choose.split()
        len_symbol_coin_choose = len(split_coin_choose)
        symbol_coin_choose = split_coin_choose[len_symbol_coin_choose-1]
        new_combobox_values = []

        for coin in all_coins:
            if symbol_coin_choose == coin[2]:
                historical_data = self.coin_data.get_historical_data(coin[2])
                historical_data_id_crypto = np.concatenate((historical_data, np.full((len(historical_data), 1), coin[0])), axis=1)

                self.historical_data_model.insert(historical_data_id_crypto)

                var_success_message.set("Les données historique de la cryptomonnaie ont été ajouté avec succès.")

        coins_not_uses = self.get_cryptocurrencies_not_uses()

        for coin_not_uses in coins_not_uses:
            new_combobox_values.append(coin_not_uses[1] + " " + coin_not_uses[2])

        combobox["values"] = new_combobox_values
        combobox.current(0)

    def delete_historical_data_crypto(self, id_cryptomonnaie):
        self.historical_data_model.delete(id_cryptomonnaie)
        self.switch_frame(self.cryptocurrency_list, self.cryptocurrency_list)


profitech_c = ProfitechController()




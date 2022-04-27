import numpy as np
from tkinter import *
from datetime import datetime

from Class.auth import Auth
from Class.coin_data import CoinData
from Class.utils import Utils
from Class.strategy import Strategy
from Class.visualization import Visualization

from View.auth_view import AuthView
from View.home_view import HomeView
from View.cryptocurrency_list_view import CryptocurrencyListView
from View.cryptocurrency_add_view import CryptocurrencyAddView
from View.analysis_view import AnalysisView
from View.analysis_result_view import AnalysisResultView

from Model.sqlite_sequence_model import SqliteSequenceModel
from Model.user_model import UserModel
from Model.cryptocurrency_model import CryptocurrencyModel
from Model.historical_data_model import HistoricalDataModel
from Model.analysis_model import AnalysisModel
from Model.portfolio_model import PortfolioModel
from Model.ordre_achat_model import OrdreAchatModel
from Model.ordre_vente_model import OrdreVenteModel


class ProfitechController:

    def __init__(self):

        # Instanciation des modèles
        self.sqlite_sequence_model = SqliteSequenceModel()
        self.user_model = UserModel()
        self.cryptocurrency_model = CryptocurrencyModel()
        self.historical_data_model = HistoricalDataModel()
        self.analysis_model = AnalysisModel()
        self.portfolio_model = PortfolioModel()
        self.ordre_achat_model = OrdreAchatModel()
        self.ordre_vente_model = OrdreVenteModel()

        # Instanciation des classes de traitements
        self.auth = Auth(self.user_model)
        self.coin_data = CoinData()
        self.utils = Utils()
        self.visualization = Visualization()

        # Création de la fenêtre
        self.window = Tk()

        self.window.title("Profitech Analysis")
        self.window.geometry("720x560")
        self.window.minsize(480, 360)
        self.window.iconbitmap("View/asset/image/logo.ico")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        # Instanciation des vues
        self.auth_view = AuthView(self)
        self.home_view = HomeView(self)
        self.cryptocurrency_list_view = CryptocurrencyListView(self)
        self.cryptocurrency_add_view = CryptocurrencyAddView(self)
        self.analysis_view = AnalysisView(self)
        self.analysis_result_view = AnalysisResultView(self)

        # portfolios = self.get_portfolios(40)
        # self.histogram(portfolios)

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
        symbol_coin_choose = split_coin_choose[0]
        new_combobox_values = []

        for coin in all_coins:
            if symbol_coin_choose == coin[1]:
                historical_data = self.coin_data.get_historical_data(coin[1])
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
        self.switch_frame(self.cryptocurrency_list_view, self.cryptocurrency_list_view)

    def strategy(self, invest_dates, coin_name, freq, price, strat, intervalle, progress_bar, id_analysis):
        historical_data = np.array(self.historical_data_model.select(coin_name))
        id_portfolio = int(self.sqlite_sequence_model.select_seq("SA_Portfolio")) + 1
        id_crypto = self.cryptocurrency_model.select_id_from_name(coin_name)

        portfolios = []
        ordre_vente = []
        ordre_achat = []
        total_invest_dates = len(invest_dates)
        index_invest_dates = 0

        for invest_date in invest_dates:
            strategy = Strategy(historical_data, freq, price, invest_date[0], invest_date[1])

            if strat == "dca":
                strategy_buying = strategy.buy_dca()
            elif strat == "va":
                strategy_buying = strategy.buy_va()

            amount_crypto = strategy_buying[0]
            total_amount_crypto = np.sum(strategy_buying[0])
            total_amount_invested = np.sum(strategy_buying[1])

            sell_values = strategy.get_sell_values(strategy.get_last_date_buy())
            sell_earn = strategy.sell_crypto(sell_values[0], total_amount_crypto)
            ordre_achat = self.create_ordre_achat(ordre_achat, strategy.get_historical_date(), strategy_buying[1], id_portfolio, id_crypto, index_invest_dates)
            ordre_vente = self.create_ordre_vente(ordre_vente, np.reshape(sell_values[1], len(sell_values[1])), sell_earn, id_portfolio, id_crypto, index_invest_dates)
            portfolios = self.create_portfolio(portfolios, freq, intervalle, strat, total_amount_crypto, total_amount_invested, id_analysis)

            self.update_progress_bar(progress_bar, (index_invest_dates * 100) / (
                        total_invest_dates + (30 * total_invest_dates / 100)))

            index_invest_dates += 1

        return [portfolios, ordre_achat, ordre_vente]

    def create_ordre_achat(self, ordre_achat, ordre_achat_date, ordre_achat_price, id_portfolio, id_crypto, index_invest_dates):

        nb_ordre_achat = range(len(ordre_achat_date))
        for index_ordre_achat in nb_ordre_achat:
            one_ordre_achat = [(id_portfolio + index_invest_dates),
                               ordre_achat_date[index_ordre_achat],
                               id_crypto,
                               float(ordre_achat_price[index_ordre_achat])]
            ordre_achat.append(one_ordre_achat)

        return ordre_achat

    def create_ordre_vente(self, ordre_vente, ordre_vente_date, ordre_vente_price, id_portfolio, id_crypto, index_invest_dates):

        nb_ordre_vente = range(len(ordre_vente_date))

        for index_ordre_vente in nb_ordre_vente:
            one_ordre_vente = [(id_portfolio + index_invest_dates),
                               ordre_vente_date[index_ordre_vente],
                               id_crypto,
                               float(ordre_vente_price[index_ordre_vente])]
            ordre_vente.append(one_ordre_vente)

        return ordre_vente

    def create_portfolio(self, portfolios, freq, intervalle, strat, total_amount_crypto, total_amount_invested, id_analysis):

        one_portfolio = [freq,
                         intervalle,
                         strat,
                         total_amount_crypto,
                         float(total_amount_invested),
                         id_analysis]

        portfolios.append(one_portfolio)

        return portfolios

    def update_progress_bar(self, progress_bar, value):
        if progress_bar["value"] < 100:
            progress_bar["value"] = value
            self.window.update_idletasks()

    def analysis(self, coin_name, strat, freq, intervalle, start_date, end_date, price, error_start_date, error_end_date, progress_bar):
        coin_begin_date = self.utils.reformat_date(self.historical_data_model.select_first_date(coin_name), "%Y-%m-%d", "%d-%m-%Y")

        if self.utils.valid_date_for_analysis(start_date, end_date, coin_begin_date, error_start_date, error_end_date):

            self.analysis_model.insert(datetime.now())
            id_analysis = self.analysis_model.select_last_id()

            if not price:
                price = 100
            else:
                price = float(price)

            if intervalle == 0:
                invest_dates = self.utils.genDateEndFixed(start_date, end_date)
            else:
                invest_dates = self.utils.genDateWithInterval(start_date, end_date, intervalle)

            portfolio_achat_vente = self.strategy(invest_dates, coin_name, freq, price, strat, intervalle, progress_bar, id_analysis)

            self.portfolio_model.insert(portfolio_achat_vente[0])
            self.update_progress_bar(progress_bar, (progress_bar["value"] + 10))

            self.ordre_achat_model.insert(portfolio_achat_vente[1])
            self.update_progress_bar(progress_bar, (progress_bar["value"] + 10))

            self.ordre_vente_model.insert(portfolio_achat_vente[2])
            self.update_progress_bar(progress_bar, 100)

            self.switch_frame(self.analysis_view, self.analysis_result_view, id_analysis)

    def get_portfolios(self, id_analyse):
        portfolios = self.portfolio_model.select(id_analyse)
        portfolios_w_buy_sold = []

        for portfolio in portfolios:
            portfolio = list(portfolio)
            ordre_achat = self.ordre_achat_model.select(portfolio[0])
            ordre_vente = self.ordre_vente_model.select(portfolio[0])
            portfolios_w_buy_sold.append([portfolio, ordre_achat, ordre_vente])

        return portfolios_w_buy_sold

    def histogram(self, portfolios):
        montant_achat = np.array([])
        for portfolio in portfolios:
            for ordre_achat in portfolio[1]:
                montant_achat = np.append(montant_achat, ordre_achat[1])

        bins = np.arange(round(np.min(montant_achat), 0), round(np.max(montant_achat), 0), 50)
        self.visualization.histogram(montant_achat, bins, self.analysis_result_view.frame)








profitech_c = ProfitechController()




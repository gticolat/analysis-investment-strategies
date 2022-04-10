from dateutil.relativedelta import relativedelta
import numpy as np
import datetime


class Strategy:
    """Classe permettant de simuler des stratégies d'achat et de ventes.

    Attributes :
        historical_data :
        (ndarray) Tableau de deux dimensions contenant les prix d'une cryptomonnaie
        à une date. Exemple : [['01-01-2015', 320.43499755859375], ['02-01-2015', 314.0790100097656]]
        temp :
        (string) Temps d'intervalle entre deux achats. Exemple : "weekly" ou "monthly"
        price :
        (float) Prix que l'on souhaite investir pour les ordres d'achats. Exemple : 400.00
        invest_start_date :
        (datetime.datetime) Date à laquelle on commence à investir. Première date d'achat.
        invest_end_date :
        (datetime.datetime) Date à laquelle on arrête d'investir.
        temp_date :
        (relativedelta) Temps à ajouter à un type datetime.datetime en fonction de
        l'attribut temp
        historical_date :
        (ndarray.datetime) Tableau de date qui correspond aux dates d'achat en fonction de
        l'attribut temp. Exemple : [[01-01-2015], [01-02-2015]]
        historical_price :
        (ndarray.float) Tableau de prix qui correspond aux dates d'achats. Exemple :
        [[320.43499755859375], [216.86700439453125]]
    """

    def __init__(self, historical_data, temp, price, invest_start_date, invest_end_date):
        self.historical_data = historical_data
        self.temp = temp
        self.price = price
        self.invest_start_date = invest_start_date
        self.invest_end_date = invest_end_date

        self.temp_date = self.create_temp_date()
        clean_historical_data = self.cleaning_historical_data(self.temp_date)
        self.historical_date = clean_historical_data[0]
        self.historical_price = clean_historical_data[1]

    def get_historical_data(self):
        return self.historical_data

    def get_historical_date(self):
        return self.historical_date

    def get_historical_price(self):
        return self.historical_price

    def get_temp(self):
        return self.temp

    def get_invest_start_date(self):
        return self.invest_start_date

    def get_invest_end_date(self):
        return self.invest_end_date

    def define_temp(self):
        """Récupération d'un intervalle à ajouter à un type datetime.

        Returns :
            (relativedelta) intervalle qui dépend de l'attribut temp
        """
        if self.temp == "weekly":
            result = relativedelta(weeks=1)

        elif self.temp == "monthly":
            result = relativedelta(days=31)

        return result

    def create_temp_date(self):
        """Création d'un tableau de date avec un intervalle entre deux dates.

        La fonction arange créé un tableau de type ndarray. Il le remplit comme suit :
        arange(départ, fin, pas). Exemple : arange(0, 6, 2) -> [0, 2, 4, 6]

        Returns :
            (ndarray.datetime) Tableau de date avec un intervalle entre deux dates
        """
        return np.arange(self.invest_start_date, self.invest_end_date, self.defineTemp()).astype(datetime.datetime)

    def cleaning_historical_data(self, temp_date):
        """Filtrage du tableau des données historique de prix.

        Args :
            temp_date :
            (relativedelta) Temps à ajouter à un type datetime.datetime en fonction de
            l'attribut temp

        Returns :
            (list) Une liste à deux dimensions qui comprend les dates d'achats et les prix.
            Exemple : [[[01-01-2015], [01-02-2015]], [[320.43499755859375], [216.86700439453125]]]
        """
        historical_price = np.array([], dtype=float)
        historical_date = np.array([], dtype=datetime.datetime)

        for temp_date_value in temp_date:
            mask = (self.historical_data[:, 0] == temp_date_value.strftime("%d-%m-%Y"))
            historical_price = np.append(historical_price, self.historical_data[mask, :][0][1].astype(np.float))
            historical_date = np.append(historical_date, self.historical_data[mask, :][0][0].astype(datetime.datetime))

        return [historical_date, historical_price]

    def sell_crypto(self, sell_values, amount_crypto_buy):
        """Vente des cryptomonnaies en fonction du prix de vente.

        Args :
            sell_values :
            (ndarray.float) Tableau de réel qui correspond aux prix de vente des cryptomonnaies
            amount_crypto_buy :
            (float) Total de cryptomonnaie qui a été acheté

        Returns :
            (ndarray.float) Une liste de la valeur du portefeuille en dollar avec la vente. Exemple :
            [11280.43, 14214.13, ...]
        """
        return sell_values * amount_crypto_buy

    def get_last_date_buy(self):
        """Récupération de la dernière date d'achat dans un tableau.

        Returns :
            (datetime.datetime) Une date qui correspond à la dernière date d'achat
        """
        return self.temp_date[len(self.temp_date) - 1]

    def get_sell_values(self, last_date_buy):
        """Récupération des valeurs de prix et dates de ventes.

        On récupère toutes les données entre la dernière date d'achat et la date
        d'aujourd'hui à partir des données historique. Chaque date de vente
        génère un nouveau cas.

        Returns :
            (list) Liste de deux ndarray, le premier concernant les prix, l'autre les dates.
            Exemple : [[[315.0854], [452.43234]], [[01-01-2017], [02-01-2017]]]
        """
        last_index = len(self.historical_data) - 1
        last_buy_index = np.where(self.historical_data == last_date_buy.strftime("%d-%m-%Y"))[0][0] + 1

        sell_price = np.array(self.historical_data[last_buy_index:last_index, 1:2], dtype=float)
        sell_date = np.array(self.historical_data[last_buy_index:last_index, 0:1], dtype=datetime.datetime)

        return [sell_price, sell_date]

    def buy_dca(self):
        """Achat avec la stratégie Dollar Cost Averaging.

        Returns :
            (list) Liste qui contient les valeurs du portefeuille en cryptomonnaie
            et en dollars. Exemple : [[[0.00452], [0.003521]], [[400], [400]]]
        """
        return [self.price / self.historical_price, np.full(self.historical_price.size, self.price)]

    def buy_va(self, value_path):
        """Achat avec la stratégie Value Averaging.

        Args :
            value_path :
            (float) Valeur du portefeuille souhaité à chaque étape d'investissement. Par exemple, on veut
            que tous les mois notre portefeuille contienne une valeur de 1000.00 $.

        Returns :
            (list) Liste qui contient les valeurs du portefeuille en cryptomonnaie
            et en dollars. Exemple : [[[0.00452], [0.003521]], [[400], [430]]]
        """
        nb_crypto_before_rebalancing = 0
        crypto_buy = 0
        value_path_x = 1
        money_invested_total = np.array([], dtype=float)
        crypto_buy_total = np.array([], dtype=float)

        for price in self.historical_price:
            crypto_buy = (((value_path * value_path_x) - (nb_crypto_before_rebalancing * price)) / price)
            money_invested = ((value_path * value_path_x) - (nb_crypto_before_rebalancing * price))
            nb_crypto_before_rebalancing += crypto_buy
            value_path_x += 1
            money_invested_total = np.append(money_invested_total, money_invested)
            crypto_buy_total = np.append(crypto_buy_total, crypto_buy)

        return [crypto_buy_total, money_invested_total]


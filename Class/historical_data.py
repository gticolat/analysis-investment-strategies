from Model.historical_data_model import HistoricalDataModel
from Model.cryptocurrency_model import CryptocurrencyModel


class HistoricalData:

    def __init__(self):
        self.historical_data_model = HistoricalDataModel()
        self.cryptocurrency_model = CryptocurrencyModel()

    # def get_historical_data(self):

    def set_historical_data(self, date_price, symbole):

        id_crypto = self.cryptocurrency_model.select_id_from_symbol(symbole)

        if id_crypto == -1:
            self.cryptocurrency_model.insert(symbole)
            id_crypto = self.cryptocurrency_model.select_id_from_symbol(symbole)

        for value in date_price:
            self.historical_data_model.insert([value[0], value[1], id_crypto])






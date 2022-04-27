import datetime

import numpy as np
from requests import get

from cryptocmd import CmcScraper


class CoinData:

    def __init__(self):
        print("")

    def get_major_coins(self):

        major_coins = np.empty((0, 4))

        api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/map?sort=cmc_rank&limit=100"

        json_data = get(api_url).json()

        for coin in json_data['data']:
            major_coins = np.append(major_coins, np.array([[coin['id'], coin['symbol'], coin['name'], coin['rank']]]), axis=0)

        return major_coins

    def get_historical_data(self, symbole):

        now = datetime.date.today()
        scraper = CmcScraper(symbole, "01-01-2015", now.strftime("%d-%m-%Y"))

        headers, historical_data = scraper.get_data()
        historical_data = np.array(historical_data)[:, 0:2]
        historical_data = np.flip(historical_data, 0)

        index = 0
        for data in historical_data:
            date = datetime.datetime.strptime(data[0], "%d-%m-%Y")
            date_format = date.strftime("%Y-%m-%d")
            historical_data[index][0] = date_format
            index += 1

        return historical_data

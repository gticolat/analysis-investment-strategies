import datetime
import numpy as np
from cryptocmd import CmcScraper
from Model.database_init import DatabaseInit
from Class.historical_data import HistoricalData

# Créer un tableau de tableau : [[date], [nbBTC], [argentInjecte]]
# Voir si on peut gérer le portefeuille avec une classe
'''

def gen_strategy_result(strategy_name, temp, interval=None):
    # On définit les dates de début et de fin d'investissement
    invest_end_date = datetime.datetime.strptime("01-01-2021", "%d-%m-%Y")
    date_start = datetime.datetime.strptime("01-01-2018", "%d-%m-%Y")

    gen_date_interval = DateInterval(date_start, invest_end_date)

    # Si l'interval n'est pas définit, on par avec une date de fin fixe
    # Sinon on génère un tableau de date avec un interval
    if interval is None:
        # Retourne un tableau sous la forme : [[date_debut, date_fin], [date_debut, date_fin], ...]
        invest_dates = gen_date_interval.genDateEndFixed()
    else:
        # Retourne un tableau sous la forme : [[date_debut, date_fin], [date_debut, date_fin], ...]
        # Avec un interval correspondant à la valeur d'interval passé en paramètre entre les deux dates
        invest_dates = gen_date_interval.genDateWithInterval(interval)

    profit_dollar = np.array([], dtype=float)
    profit_percent = np.array([], dtype=float)
    portfolios = []

    for invest_date in invest_dates:

        strategy = Strategy(historical_data, temp, 100, invest_date[0], invest_date[1])

        if strategy_name == "dca":
            strategy_buying = strategy.buyDca()

        elif strategy_name == "va":
            strategy_buying = strategy.buyVa(100)

        amount_crypto = strategy_buying[0]
        total_amount_crypto = np.sum(strategy_buying[0])
        total_amount_invested = np.sum(strategy_buying[1])

        sell_values = strategy.getSellValues(strategy.getLastDateBuy())
        sell_price = sell_values[0]
        sell_date = sell_values[1]

        sell_earn = strategy.sellCrypto(sell_price, total_amount_crypto)

        nb_sell = range(len(sell_earn))
        for index in nb_sell:
            one_portfolio = Portfolio(strategy.get_historical_date(), amount_crypto, np.sum(strategy.money_invested()),
                                      sell_date[index], sell_earn[index])
            portfolios.append(one_portfolio)

    return portfolios

'''
crypto_symbole = "ETH"

now = datetime.date.today()
# initialise scraper without time interval
scraper = CmcScraper(crypto_symbole, "01-01-2015", now.strftime("%d-%m-%Y"))

interval_total = np.array([], dtype=int)

# get raw data as list of list
headers, historical_data = scraper.get_data()
historical_data = np.array(historical_data)[:, 0:2]
historical_data = np.flip(historical_data, 0)
'''
# Date de fin fixe fréquence mois
portfolios_dca_monthly_no_interval = gen_strategy_result("dca", "monthly")
# portfolios_weekly_no_interval = gen_dca_result("weekly")

portfolios_va_monthly_no_interval = gen_strategy_result("va", "monthly")

# période de 3 mois fréquence semaine
interval = 3
# portfolios_monthly_3_months = gen_dca_result("monthly", interval)
# portfolios_weekly_3_months = gen_dca_result("weekly", interval)
#
# # période de 6 mois fréquence semaine
interval = 6
#portfolios_monthly_6_months = gen_dca_result("monthly", interval)
#portfolios_weekly_6_months = gen_dca_result("weekly", interval)
#
# # période de 12 mois fréquence semaine
interval = 12
#portfolios_monthly_12_months = gen_dca_result("monthly", interval)
#portfolios_weekly_12_months = gen_dca_result("weekly", interval)

# Faire une courbe du profit (dollar, percent) en fonction de la durée d'intervalle (pour chaque strat)

invest_visualization = Visualization()

invest_visualization.portfolio_heatmap_profit(portfolios_dca_monthly_no_interval, 'portfolios_dca_monthly_no_interval.png')
invest_visualization.portfolio_heatmap_profit(portfolios_va_monthly_no_interval, 'portfolios_va_monthly_no_interval.png')

# invest_visualization.portfolio_heatmap_profit(portfolios_monthly_3_months, 'portfolios_monthly_3_months.png')
# invest_visualization.portfolio_heatmap_profit(portfolios_weekly_3_months, 'portfolios_weekly_3_months.png')

# invest_visualization.portfolio_heatmap_profit(portfolios_monthly_6_months, 'portfolios_monthly_6_months.png')
# invest_visualization.portfolio_heatmap_profit(portfolios_weekly_6_months, 'portfolios_weekly_6_months.png')

# invest_visualization.portfolio_heatmap_profit(portfolios_monthly_12_months, 'portfolios_monthly_12_months.png')
# invest_visualization.portfolio_heatmap_profit(portfolios_weekly_12_months, 'portfolios_weekly_12_months.png')

# invest_visualization.averageProfitTotal(["DCA Monthly"], [profit_percent_monthly], [profit_dollar_monthly])

# invest_visualization.profit_percent_by_interval(interval_total, [profit_percent_weekly_3months, profit_percent_weekly_6months, profit_percent_weekly_12months])

'''


#historical_data_object = HistoricalData()
#
#historical_data_object.set_historical_data(historical_data, crypto_symbole)


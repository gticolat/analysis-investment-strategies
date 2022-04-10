class GenStrategyResult:

    def test(self):
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